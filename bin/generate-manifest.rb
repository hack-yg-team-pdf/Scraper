#!/usr/bin/ruby

IN_PATH = "#{File.dirname(__FILE__)}/../data/all-forms.html".freeze
OUT_PATH = 'all-forms.json'.freeze

PROJECT_ROOT = "./#{File.dirname(__FILE__)}/..".freeze

require 'nokogiri'
require 'pry'
require 'json'
require "#{PROJECT_ROOT}/lib/all_forms_parser.rb"

doc = File.open(IN_PATH) { |f| Nokogiri::HTML(f) }

anchor = doc.css('h2').first.parent # closest div that contains all h2's and headers

my_enum = anchor.children.to_enum
parsed_results = {}

my_parser = AllFormsParser.new

begin
  while true
    while true
      last_element = my_enum.next
      break if last_element.name == 'h2'
    end
    section_header = last_element
    section_label = section_header.children[0].to_s
    puts "Found section #{section_label}!"

    my_enum.next # drop one
    table = my_enum.next # now we've got the table
    parsed_results[section_label] = my_parser.parse_table(table).map { |r| r.as_json }
  end
rescue StopIteration => _
end

File.open(OUT_PATH, 'w') { |f| f.puts JSON.pretty_generate(parsed_results) }
