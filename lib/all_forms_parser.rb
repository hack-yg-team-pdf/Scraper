class Form
  attr_accessor :id, :label, :url_english, :url_french
  def initialize(id, label, url_bilingual: nil, url_english: nil, url_french: nil)
    self.id = id
    self.label = label

    self.url_english = url_english
    self.url_french = url_french

    if url_bilingual
      self.url_english = url_bilingual
      self.url_french = url_bilingual
    end
  end

  def bilingual?
    url_english == url_french
  end

  def ==(other)
    id == other.id && label == other.label && url_french == other.url_french && url_english == other.url_english
  end
end

class AllFormsParser
  def nbsp
    @nbsp ||= Nokogiri::HTML('&nbsp;').text
  end

  def parse_one_line(line)
    label = line.children[0].to_s.strip.strip
    label = label.gsub(/^#{nbsp}*/, '')
    label = label.gsub(/#{nbsp}*$/, '')

    links = line.children[2].css('a')

    if links.length == 1
      anchor_english = links[0]
      anchor_french  = links[0]
    else
      anchor_english, anchor_french = links
    end

    url_english = anchor_english.attributes['href'].value.strip
    url_french = anchor_french.attributes['href'].value.strip
    id = /(yg[\d]{4})/.match(url_english)[1]

    Form.new(id, label, url_english: url_english, url_french: url_french)
  end
end
