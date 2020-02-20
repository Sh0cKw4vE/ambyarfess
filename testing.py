import re

pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
s = "Mi grupo favorito de CRIMINALISTICA. Ultima clase de cuatrimestre https://t.co/Ad2oWDNd4u"
print(pattern.sub('', s))
mediasource = pattern.findall(s)
print(mediasource)
