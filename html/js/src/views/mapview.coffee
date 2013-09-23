#!/usr/bin/env coffee

class MapView extends Backbone.View
  settings:
    zoomLevel:
      'wide' : 4
      'default': 10
      'close': 14
      'tight' : 21
      'increment' : 1

  model: Location

  mapOptions:
    #TODO styled maps?
    #https://developers.google.com/maps/documentation/javascript/styling#creating_a_styledmaptype
    zoom: 4
    #google.maps.MapTypeId.SATELLITE | ROADMAP | HYBRID
    mapTypeId: google.maps.MapTypeId.ROADMAP
    mapTypeControlOptions:
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
    minZoom: 1
    zoomControl: true
    zoomControlOptions:
      style: google.maps.ZoomControlStyle.DEFAULT
      position: google.maps.ControlPosition.TOP_LEFT
    panControlOptions:
      position: google.maps.ControlPosition.TOP_LEFT

  googlemap: (id)->
    @gmap = new google.maps.Map(document.getElementById(id), @mapOptions)
    google.maps.event.addListener(@gmap, 'click', (event) =>
      @handleMapClick(event)
    )
    return @gmap

  marker: ->
    return new google.maps.Marker()

  infowindow: ->
    return new google.maps.InfoWindow()

  mappoint: (latitude, longitude)->
    return new google.maps.LatLng(latitude, longitude)

  markerFromMapLocation: (map, location)->
    markerSettings =
      position: location
      map: map
      animation: google.maps.Animation.DROP
      draggable: true
    return new google.maps.Marker(markerSettings)

  updateInfoWindow: (text, location, @map = @googlemap()) ->
    infowindow = @infowindow()
    infowindow.setContent(text)
    infowindow.setPosition(location)
    infowindow.open(map)

  setUserPlaceFromLocation: (location) ->
    @userPlace = location

  showInfowindowFormAtLocation: (map, marker, location) ->
    @userInfowindow.close() if @userInfowindow?
    @userInfowindow = @infowindow()
    @userInfowindow.setContent(document.getElementById('iwcontainer').innerHTML)
    @userInfowindow.setPosition(location)
    @userInfowindow.open(map)

  clearMapMarker: (marker) ->
    marker.setMap(null)
    marker = null

  initialize: ->
    @userMapsMarker = null
