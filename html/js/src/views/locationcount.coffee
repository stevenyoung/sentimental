#!/usr/bin/env coffee

class Countview extends Backbone.View
  el: '#count'
  model: Location
  count: null

  initialize: () ->
    locs = new Locations()
    locs.url = '/places/count'
    locs.fetch({
      error: (model, response) ->
        console.log('fetch error', error)
      success: (model, response) =>
        @setCount(response.count)
        @showCount()
      })

  setCount: (count) ->
    @count = count

  showCount: () ->
    $(@el).text(@count + ' scenes have been mapped')