data =[{"id"=>"1", "price"=>"1.1027", "change"=>"+0.0006", "chg_per"=>"+0.05%", "last_changed"=>"2019-11-25 06:47:07", "symbol"=>"EUR/USD"}, {"id"=>"20", "price"=>"108.87", "change"=>"+0.23", "chg_per"=>"+0.21%", "last_changed"=>"2019-11-25 06:39:09", "symbol"=>"USD/JPY"}, {"id"=>"41", "price"=>"1.2817", "change"=>"+0.0022", "chg_per"=>"+0.18%", "last_changed"=>"2019-11-25 06:49:14", "symbol"=>"GBP/CHF"}]
require 'nokogiri'

text= ''
data.each do |key, value|
    key.each do |key, value|
        text << "#{key}: #{value} " 
    end
end
p text


# while true do
#     p 'hello'
#     sleep 2
# end

$jim = true

p "#{$jim}ssssssssssssssssssssss"

def jim
    # p $jim
     while $jim do
         print "hello #{$jim}"
     end
end

jim