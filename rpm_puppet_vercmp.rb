#!/usr/bin/env ruby
require 'rpmvercmp'

Rpmvercmp.debug = false
rc = Rpmvercmp.compare_labels ARGV[0], ARGV[1]

if rc == -1
  puts "#{ARGV[0]} < #{ARGV[1]}"
elsif rc == 1
  puts "#{ARGV[0]} > #{ARGV[1]}"
else
  puts "#{ARGV[0]} = #{ARGV[1]}"
end
