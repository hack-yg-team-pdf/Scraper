class Form
  attr_accessor :id, :label, :url_english, :url_french, :section
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

  def as_json
    r = {
      id: id,
      label: label,
      url_english: url_english,
      url_french: url_french
    }
    r[:section] = section if section
    r
  end
end

class AllFormsParser
  def nbsp
    @nbsp ||= Nokogiri::HTML('&nbsp;').text
  end

  def strip(my_string)
    my_string = my_string.strip
    my_string = my_string.gsub(/^#{nbsp}*/, '')
    my_string = my_string.gsub(/#{nbsp}*$/, '')
    my_string
  end

  def parse_one_line(line)
    label = strip(line.children[0].to_s)
    links = line.children[2].css('a')

    return nil if links.length == 0
    
    if links.length == 1
      anchor_english = links[0]
      anchor_french  = links[0]
    else
      anchor_english, anchor_french = links
    end

    url_english = anchor_english.attributes['href'].value.strip
    url_french = anchor_french.attributes['href'].value.strip
    id_match = /(yg[\d]{4})/.match(url_english)
    if id_match.nil?
      return nil
    end

    id = id_match[0]
    Form.new(id, label, url_english: url_english, url_french: url_french)
  end

  def take_until(enum)
    all_values = []
    begin
      while !yield(enum.peek)
        all_values << enum.next
      end
    rescue StopIteration => _
    end
    all_values
  end

  def parse_table(table)
    content = table.children[1].children[1].children
    my_enum = content.to_enum
    all_forms = []
    dropped_elements = take_until(my_enum) { |e| e.name == 'h3' } # advance to first section
    begin
      while my_enum.peek # loop over sections
        section_header_element = my_enum.next
        section_header = strip(section_header_element.text)

        this_sections_elements = take_until(my_enum) { |e| e.name == 'h3' }
        this_sections_forms = this_sections_elements.select { |e| e.name == 'p' }.map { |p| parse_one_line(p) }.compact
        this_sections_forms.each { |f| f.section = section_header }
        all_forms += this_sections_forms
      end
    rescue StopIteration => _
    end

    all_forms
  end
end
