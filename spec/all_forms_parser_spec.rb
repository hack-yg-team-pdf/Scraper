require 'spec_helper'

require 'all_forms_parser'
require 'nokogiri'
require 'pry'

def nokogiri(html_fragment)
  r = Nokogiri::HTML(html_fragment)
  r = r.children[1] # document
  r = r.children[0] # html
  r = r.children[0] # body
  r
end

RSpec.describe AllFormsParser do
  describe '#parse_one_line' do
    context 'html is one bilingual example' do
      let(:example) do
        nokogiri(<<-HTML)
        <p>&nbsp;Request for Access to Records <br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="http://www.gov.yk.ca/forms/images/arrow_r_2.gif">&nbsp;&nbsp; <a href="

        http://www.gov.yk.ca/forms/forms/4500/yg4552_b.pdf" target="blank">Bilingual</a> <img src="http://www.gov.yk.ca/forms/images/filetype_pdf.jpg" alt="PDF"> (YG4552)</i></p>
        HTML
      end

      it 'pulls the required record' do
        expect(subject.parse_one_line(example)).to eq(
          Form.new(
            'yg4552',
            'Request for Access to Records',
            url_bilingual: 'http://www.gov.yk.ca/forms/forms/4500/yg4552_b.pdf'
          )
        )
      end
    end

    context 'html contains an english and french form' do
      let(:example) do
        nokogiri(<<-HTML)
        <p>&nbsp;Accessing Adoption Records - Application for Service <br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="http://www.gov.yk.ca/forms/images/arrow_r_2.gif">&nbsp;&nbsp; <a href="
http://www.gov.yk.ca/forms/forms/5500/yg5654_e.pdf" target="blank">English</a> <a href="
http://www.gov.yk.ca/forms/forms/5500/yg5654_f.pdf" target="blank">French</a> <img src="http://www.gov.yk.ca/forms/images/filetype_pdf.jpg" alt="PDF"> (YG5654)</i></p>
        HTML
      end

      it 'pulls the required record' do
        expect(subject.parse_one_line(example)).to eq(
          Form.new(
            'yg5654',
            'Accessing Adoption Records - Application for Service',
            url_english: 'http://www.gov.yk.ca/forms/forms/5500/yg5654_e.pdf',
            url_french: 'http://www.gov.yk.ca/forms/forms/5500/yg5654_f.pdf'
          )
        )
      end
    end
  end
end
