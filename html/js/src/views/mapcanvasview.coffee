#!/usr/bin/env coffee

class MapCanvasView extends MapView
  el: 'map_canvas'
  locations: null
  userInfowindow: null
  placeInfowindow: null

  handleMapClick: (event) ->
    @setUserMapMarker(@gmap, event.latLng)

  setUserMapMarker: (map, location) ->
    @userMapsMarker.setMap(null) if @userMapsMarker?
    @userInfowindow.close() if @userInfowindow?
    @userMapsMarker = @markerFromMapLocation(map, location)
    @userMapsMarker.setMap(map)
    google.maps.event.addListener(@userMapsMarker, 'click', (event) =>
      @isUserLoggedIn()
    )

  isUserLoggedIn: () ->
    $.ajax
      datatype: 'json',
      url: '/user/status',
      success: (data) =>
        if data.status == 'logged in'
          @dropMarkerForNewLocation()
        else
          @showLoginInfoWindow()

  showLoginInfoWindow: () ->
    @userInfowindow.close() if @userInfowindow?
    @userInfowindow = @infowindow()
    content = '<div id="maplogin">'
    content += '<div>You must be logged in to add content.</div>'
    login_url = document.getElementById('loginlink').href
    content += '<a href="' + login_url + '"><button>log in</button></a></p>'
    @userInfowindow.setContent(content)
    @userInfowindow.setPosition(@userMapsMarker.getPosition())
    @userInfowindow.open(@gmap)

  dropMarkerForNewLocation: () ->
    location = @userMapsMarker.getPosition()
    @showInfowindowFormAtLocation(@gmap, @userMapsMarker, location)
    @setUserPlaceFromLocation(location)
    @handleInfowindowClick()

  updateInfowindowWithMessage: (infowindow, text) ->
    textcontainer = '<div id="thankswindow">' + text.message + '</div>'
    infowindow.setContent(textcontainer)
    google.maps.event.addListener(infowindow, 'closeclick', () =>
      @showUpdatedMap()
    )

  showUpdatedMap: () ->
    m = new MapCanvasView
    locations = new Locations()
    locations.fetch({
      error: (model, response) ->
        console.log('error', model, response)
      success: (model, response) ->
        m.mapMarkers(response)
        m.locations = response
    })

  handleInfowindowClick : (location)->
    $addPlaceButton = $('#map_canvas .infowindowform').find('.btn')
    $addPlaceButton.on('click', @addPlace) if $addPlaceButton?

  addPlace: (event) =>
    form_data =
      title: $('#title').val()
      author: $('#author').val()
      place_name: $('#place_name').val()
      date: $('#date').val()
      actors: $('#actors').val()
      symbols: $('#symbols').val()
      scene: $('#scene').val()
      notes: $('#notes').val()
      image_url: $('#image_url').val()
      check_in: $('#check_in').prop('checked')
    form_data.latitude = @userPlace.lat()
    form_data.longitude = @userPlace.lng()
    location = new Location()
    status = location.save(
      form_data,
        error: (model, xhr, options) =>
          console.log('error', model, xhr, options)
        success: (model, response, options) =>
          @updateInfowindowWithMessage(@userInfowindow, response)
    )

  geocoderSearch: () ->
    address = document.getElementById('gcf').value
    if address
      geocoder = new google.maps.Geocoder()
      geocoder.geocode({'address':address}, (results, status) =>
        if (status == google.maps.GeocoderStatus.OK)
          position = results[0].geometry.location
          @gmap.setCenter(position)
          @gmap.setZoom(@settings.zoomLevel.default)
          # @setUserMapMarker(@gmap, position)
        else
          alert("geocode was not successful: " + status)
      )

  attachSearchHandler: ->
    document.getElementById('gcf').addEventListener('keydown',
      (event) =>
        if (event.which == 13 || event.keyCode == 13)
          event.preventDefault()
          @geocoderSearch()
      )
    document.getElementById('search').addEventListener 'click', (event) =>
      @geocoderSearch()

  mapMarkers: (locations) ->
    @googlemap('map_canvas')
    @dropMarkerForStoredLocation(location) for location in locations
    if CENTER?
      mapcenter = new google.maps.LatLng(CENTER.lat, CENTER.lng)
      @gmap.setCenter(mapcenter)
      @gmap.setZoom(@settings.zoomLevel.close)
    else
      usacenterCoords =
        lat: 39.8282
        lng: -98.5795
      usacenter = new google.maps.LatLng(usacenterCoords.lat, usacenterCoords.lng)
      @gmap.setCenter(usacenter)

  dropMarkerForStoredLocation: (location) ->
    infowindowContentFromStoredLocation = (data, updateButton) ->
      field_format = '<br/><span class="pllabel"><%= label %></span>'
      two_line_format = field_format + '<br/><span class="plcontent"><%= content %></span>'
      field_format += '<span class="plcontent"><%= content %></span>'
      button_format = '<br><button class="btn visited" id="<%=place_id %>">'
      button_format += 'check-in</span></label>'
      image_format = '<img src="<%= image_url %>">'
      infotemplate = _.template(field_format)
      split_line_info = _.template(two_line_format)
      content = '<div class="plinfowindow">'
      content += '<span class="lead">' + data.title + ' by ' + data.author + '</span>'
      if !!data.place_name
        content += infotemplate({label:'location', content:data.place_name})
      if !!data.scene_time
        content += infotemplate({label:'time', content:data.place_time})
      if !!data.actors
        content += infotemplate({label:'characters', content:data.actors})
      if !!data.symbols
        content += infotemplate({label:'symbols', content:data.symbols})
      if !!data.description
        content += split_line_info({label:'description', content:data.description})
      if !!data.notes
        content += infotemplate({label:'visits', content:data.visits})
      if !!data.date_added
        content += infotemplate({label:'added', content:data.date_added})
      if !!data.image_url
        content += _.template(image_format, image_url:data.image_url)
      if updateButton
        content += _.template(button_format, place_id:data.id )
      content += '</div>'
      return content
    pos = new google.maps.LatLng location.latitude, location.longitude
    markerParams =
      position: pos
      draggable: false
      animation: google.maps.Animation.DROP
      icon : '/img/book.png'
      title : "#{ location.title } by #{ location.author }"
    marker = new google.maps.Marker(markerParams)
    marker.setMap(@gmap)
    google.maps.event.addListener marker, 'click', =>
      url = '/places/info/' + location.db_key
      $.getJSON url, (data) =>
        @placeInfowindow.close() if @placeInfowindow?
        iw = new google.maps.InfoWindow()
        iw.setContent(infowindowContentFromStoredLocation(data, true))
        iw.open(@gmap, marker)
        @placeInfowindow = iw
        $('#map_canvas').on 'click', '.visited', (event) ->
          $('.visited').hide()
          iw.setContent('updating...')
          $.getJSON '/places/visit/'+this.id, (data) =>
            iw.setContent(infowindowContentFromStoredLocation(data, false))

  handleInputAttributes: ->
    fields = $('#iwcontainer input')
    dealWithIE9Inputs = (element) ->
      inputElement.setAttribute('value', inputElement.getAttribute('placeholder'))
      inputElement.addEventListener('focus', => @value = '')
    dealWithIE9Inputs(field) for field in fields

  initialize: () ->
    this.$el.height($(window).height() - $('toolbar').height())

    places = new Locations
    places.fetch({
      error: (model, response) ->
        console.log('error', response)
      success: (model, response) =>
        @mapMarkers(response)
        @locations = response
    })

    @showInfowindowFormAtLocation()
    @attachSearchHandler()
