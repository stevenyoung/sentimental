#!/usr/bin/env coffee

class LocationToolbarView extends MapView
  model: Location

  el: document.getElementById('toolbar')

  events:
    'click #update': 'handleUserUpdate'
    'click #show': 'showSharedLocations'
    'click #share': 'shareUserLocation'

  shareUserLocation: (event)->
    ##console.log('location toolbar view share user location', event, this,
    #            event.target, event.currentTarget)
    navigator.geolocation.getCurrentPosition (position) =>
      #console.log('share pos:', position)
      $.ajax
        url: '/locate/share'
        data:
          latitude: position.coords.latitude
          longitude: position.coords.longitude
        type: 'POST'
        success: (res, status, xhr) ->
          #console.log(res, status, xhr)

  getUserLocation: ->
    navigator.geolocation.getCurrentPosition (position) =>
      #console.log('pos:', position)
      latitude = position.coords.latitude
      longitude = position.coords.longitude
      location = new google.maps.LatLng(latitude, longitude)
      contentString = "(w3c location) lat:" + latitude + " lon:" + longitude
      #console.log('str', contentString)

  showUserLocation: ->
    ##console.log('location toolbar view show user location', event, this,
    #            event.target, event.currentTarget)
    navigator.geolocation.getCurrentPosition (position) =>
      #console.log('pos:', position)
      latitude = position.coords.latitude
      longitude = position.coords.longitude
      location = new google.maps.LatLng(latitude, longitude)
      contentString = "(w3c location) lat:" + latitude + " lon:" + longitude
      #console.log('str', contentString)
      #console.log('user update map')
      mapOpts =
        location: location
        coords:
          lat: latitude
          lng: longitude
        infotext: contentString
        tilt: 45
        heading: 90
      @updateMap(mapOpts)

  handleUserUpdate: ->
    userLocation = @showUserLocation()

  initialize: ->
