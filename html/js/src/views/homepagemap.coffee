#!/usr/bin/env coffee

class HomepagemapView extends MapView
  el: 'hpmap'
  locations: null
  settings:
    zoomLevel:
      'homepagedefault': 14

  cities:
    'newhaven':
      lat: 41.3060969411
      lng: -72.9260498285
    'duluth':
      lat: 46.7833
      lng: -92.1064
    'sanfrancisco':
      lat: 37.7750
      lng: -122.4183

  googlemap: (id)->
    @mapOptions.disableDefaultUI = 'true'
    super(id)


  mapMarkers: (locations) ->
    @googlemap('hpmap')
    @dropMarkerForStoredLocation(location) for location in locations
    mapcenter = new google.maps.LatLng(@cities.newhaven.lat, @cities.newhaven.lng)
    @gmap.setCenter(mapcenter)
    @gmap.setZoom(@settings.zoomLevel.homepagedefault)

  dropMarkerForStoredLocation: (location) ->
    #TODO use templating silly man
    # infowindowContentFromStoredLocation = (data, updateButton) ->
    #   content = data.title + ' by ' + data.author
    #   content += '<br/><i>location</i> ' + data.place_name if !!data.place_name
    #   content += '<br/><i>time</i> ' + data.scene_time if !!data.scene_time
    #   content += '<br/><i>characters</i> ' + data.actors if !!data.actors
    #   content += '<br/><i>symbols</i> ' + data.symbols if !!data.symbols
    #   content += '<br/><i>description</i> ' + data.description if !!data.description
    #   content += '<br/><i>notes</i> ' + data.notes if !!data.notes
    #   content += '<br/><i>visits</i> : ' + data.visits
    #   content += '<br/><i>added</i> ' + data.date_added
    #   content += '<br><span class="btn visited" id="' + data.id + '">check-in</span></label>' if updateButton
    #   content += '<br><img src="' + data.image_url + '"/>' if data.image_url
    #   return content
    pos = new google.maps.LatLng location.latitude, location.longitude
    markerParams =
      position: pos
      draggable: false
      animation: google.maps.Animation.DROP
      icon : '/img/book.png'
      title : "#{ location.title } by #{ location.author }"
    marker = new google.maps.Marker(markerParams)
    marker.setMap(@gmap)
    # google.maps.event.addListener marker, 'click', =>
    #   url = '/places/info/' + location.db_key
    #   $.getJSON url, (data) =>
    #     iw = new google.maps.InfoWindow()
    #     iw.setContent(infowindowContentFromStoredLocation(data, true))
    #     iw.open(@gmap, marker)

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

    # @showInfowindowFormAtLocation()
    # @attachSearchHandler()