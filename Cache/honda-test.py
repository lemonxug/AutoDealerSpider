from lxml import etree

t = '''
<option value="0">请选择城市</option>
<option value='安顺' city_id='5759'>安顺</option>
<option value='凯里' city_id='5
704'>凯里</option><option value='六盘水' city_id='5699'>六盘水</option><option value='都匀' city_id='6006'>都匀</option><
option value='遵义' city_id='5953'>遵义</option><option value='兴义' city_id='5701'>兴义</option><option value='贵阳' cit
y_id='5943'>贵阳</option><option value='铜仁' city_id='5969'>铜仁</option><option value='毕节' city_id='5842'>毕节</optio
n>
'''

h = etree.HTML(t)
for c in h.xpath('//option'):
    print(c.xpath('./@value'))
    print(c.xpath('./@city_id'))