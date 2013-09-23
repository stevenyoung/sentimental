#!/usr/bin/env coffee

class RecentPlaces extends Backbone.View
  model: Location
  el: '#recentcontent'
  $list: null

  getPlaceLink: (place) ->
    console.log('new link')
    li = document.createElement('li')
    # @$list.append(li)
    li.id = place.db_key
    # li.addEventListener('click', (event) =>
    #   @getPlaceDetails(event)
    # )
    link = document.createElement('a')
    link.href = '/map/' + place.latitude + ',' + place.longitude
    link.textContent = place.title + ': ' + place.location
    li.appendChild(link)
    console.log(li)
    return li

  getPlaceDetails: (event) ->
    url = '/places/info/' + event.target.id
    $.getJSON url, (data) =>
      @showPlacesDetails(data)

  showPlacesDetails: (data) ->
    console.log('show places', data)
    $details = $('#homedetail')
    content = '<p>' + data.title + ' by ' + data.author
    content += '<br/><i>location</i> ' + data.placename if !!data.placename
    content += '<br/><i>time</i> ' + data.scenetime if !!data.scenetime
    content += '<br/><i>characters</i> ' + data.actors if !!data.actors
    content += '<br/><i>symbols</i> ' + data.symbols if !!data.symbols
    content += '<br/><i>description</i> ' + data.description if !!data.description
    content += '<br/><i>notes</i> ' + data.notes if !!data.notes
    content += '<br/><i>visits</i> : ' + data.visits
    content += '<br/><i>added</i> ' + data.dateadded + '</p>'
    content += '<br><img src="' + data.image_url + '"/>' if data.image_url
    $details.html(content)

  showRecentPlaces: (data) ->
    # use a fragment as a container
    # build a list
    listFragment = document.createDocumentFragment()
    @$list.find('li').remove()
    console.log(data)
    listItems = (@getPlaceLink(location) for location in data)
    console.log('list items', listItems)
    listFragment.appendChild(link) for link in listItems
    @$list.append(listFragment)
    return listFragment

  initialize: () ->
    @$list = @$('ul')
    locations = new Locations()
    locations.url = '/places/recent'
    locations.fetch({
      error: (model, response) ->
        console.log('error', response)
      success: (model, response) =>
        @locations = response
        console.log('fetched', response)
        @showRecentPlaces(response)
    })
