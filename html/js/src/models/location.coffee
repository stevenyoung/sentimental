#!/usr/bin/env coffee

class Location extends Backbone.Model
  defaults:
    title: 'Put Title Here'
    author: 'Someone\'s Name goes here'

  url: '/places/add'

class Locations extends Backbone.Collection
  model: Location

  # url: '/places/show'
  url: 'places.json'
  #parse: (response) ->
  #  console.log 'inside locations collection parse'
  #  buildMapPoint = (location) ->
  #    point = new google.maps.LatLng(location.latitude, location.longitude)
  #    #console.log('point', point)
  #  points = (buildMapPoint(location) for location in response)
  #  console.log 'points', points, response

  initialize: ->
    this.on 'add', (model)->
      alert 'adding model'