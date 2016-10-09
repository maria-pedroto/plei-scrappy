import scrapy


class DgsiSpider(scrapy.Spider):
  name = "dgsi"
  start_urls=['http://www.dgsi.pt/jtrp.nsf?OpenDatabase']
  _prev_page=None
  STOP_AT=5000

  def parse(self, response):
    param=response.url.split("=")
    if len(param)>1:
      start = param[-1]
    else:
      start=1
    #prev=response.css('body table:first_child tr td div a::attr(href)')[7].extract()
    next=response.css('body table:first_child tr td div a::attr(href)')[8].extract()    
    #filename = 'dl-%s.html' % start
    #with open(filename, 'wb') as f:
    #    f.write(response.body)
    if int(start) > self.STOP_AT:
      return
    self.log('checked start %s' % start)
    acordaos=response.css('table tr td table tr td font a::attr(href)')
    for ac_url in acordaos:
      full_ac_url = response.urljoin(ac_url.extract())
      yield scrapy.Request(full_ac_url, callback=self.parse_acordao)
    if next!=self._prev_page:
      self._prev_page=next
      yield scrapy.Request(response.urljoin(next), callback=self.parse)

      
  def parse_acordao(self, response):
  
    ret= {
      'url': response.url
    }
    
    for linha in response.css('body > table > tr')[1:]:
      if linha.css('img'):
        continue
      name=linha.css('td:nth_child(1) b font::text').extract_first().strip(':')
      content=''.join(linha.css('td:nth_child(2) *::text').extract())
      ret[name]=content
    
    yield ret
