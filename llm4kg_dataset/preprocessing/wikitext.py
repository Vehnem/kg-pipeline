import re
import xml.etree.ElementTree as ET

def extract_infobox(wikitext):
    infobox_pattern = r"{{Infobox[\s\S]*?}}"
    key_value_pattern = r"\|\s*(.*?)\s*=(.*)"

    infobox_match = re.search(infobox_pattern, wikitext)
    if infobox_match:
        infobox_text = infobox_match.group(0)
        key_value_matches = re.findall(key_value_pattern, infobox_text)
        print(key_value_matches)
        infobox_dict = {key.strip(): value.strip() for key, value in key_value_matches}
        return infobox_dict
    else:
        return {}

# Example usage
wikitext = """
{{Infobox film
| name           = Titanic
| image          = Titanic (1997 film) poster.png
| alt            = The film poster shows a man and a woman hugging over a picture of the Titanic's bow. In the background is a partly cloudy sky and at the top are the names of the two lead actors. The middle has the film's name and tagline, and the bottom contains a list of the director's previous works, as well as the film's credits, rating, and release date.
| caption        = Theatrical release poster
| director       = [[James Cameron]]
| producer       = {{plainlist|
* James Cameron
* [[Jon Landau (film producer)|Jon Landau]]
}}
| writer         = James Cameron
| starring = {{Plainlist|
* [[Leonardo DiCaprio]]
* [[Kate Winslet]]
* [[Billy Zane]]
* [[Kathy Bates]]
* [[Frances Fisher]]
* [[Bernard Hill]]
* [[Jonathan Hyde]]
* [[Danny Nucci]]
* [[David Warner (actor)|David Warner]]
* [[Bill Paxton]]}}&lt;!--Per billing block – Note: Gloria Stuart and Victor Garber are not included in the billing block and therefore not listed here. --&gt;
| music          = [[James Horner]]
| cinematography = [[Russell Carpenter]]
| editing        = {{plainlist|
* [[Conrad Buff IV|Conrad Buff]]
* James Cameron
* [[Richard A. Harris]]
}}
| studio         = {{plainlist|
* [[Paramount Pictures]]&lt;ref name=BFI&gt;{{cite web|title=Titanic (1997)|work=Film &amp; TV Database|publisher=[[British Film Institute]] |url=http://ftvdb.bfi.org.uk/sift/title/541102|archive-url=https://web.archive.org/web/20090114204629/http://ftvdb.bfi.org.uk/sift/title/541102|archive-date=January 14, 2009|access-date=July 29, 2011}}&lt;/ref&gt;&lt;ref name="AFI Catalog"&gt;{{cite web |title=Titanic |work=[[AFI Catalog of Feature Films]] |publisher=[[American Film Institute]] |url=https://catalog.afi.com/Catalog/moviedetails/55202 |access-date=February 2, 2018 |archive-date=September 15, 2020 |archive-url=https://web.archive.org/web/20200915062543/https://catalog.afi.com/Catalog/moviedetails/55202 |url-status=live }}&lt;/ref&gt;
* [[20th Century Fox]]&lt;ref name=BFI/&gt;&lt;ref name="AFI Catalog" /&gt;
* [[Lightstorm Entertainment]]&lt;ref name=BFI/&gt;
}}
| distributor    = {{plainlist|
* Paramount Pictures&lt;br /&gt;(United States and Canada)
* [[20th Century Fox]]&lt;br /&gt;(International)
}}
| released       = {{Film date|1997|11|01|[[Tokyo International Film Festival|Tokyo]]|1997|12|19|United States}} &lt;!-- PLEASE DO NOT ADD THE 2012 RE-RELEASE DATE, AS WELL AS THE 2017 AND 2023 RE-RELEASE DATE! WP:FILM guidelines dictate we must use the earliest and country of origin release dates. Any attempts to add an international airdate will be removed, but can be added in the release section. Thank you.--&gt;
| runtime        = 195 minutes&lt;!--Theatrical runtime: 194:36--&gt;&lt;ref&gt;{{cite web | url=https://www.bbfc.co.uk/release/titanic-q29sbgvjdglvbjpwwc0zmdu3oty | title=''TITANIC'' (12) | work=[[British Board of Film Classification]] | date=November 14, 1997 | access-date=November 8, 2014 | archive-date=April 27, 2021 | archive-url=https://web.archive.org/web/20210427093725/https://www.bbfc.co.uk/release/titanic-q29sbgvjdglvbjpwwc0zmdu3oty | url-status=live }}&lt;/ref&gt;
| country        = United States
| language       = English
| budget         = $200&amp;nbsp;million&lt;ref name="Garrett (2007)"/&gt;&lt;ref name="Sandler &amp; Studlar 1999"/&gt;&lt;ref name="Welkos (1998)"/&gt; 
| gross          = $2.257&amp;nbsp;billion{{refn|group=Note|name="BoxOfficeCorrection"|The totals given for ''Titanic'' at [[Box Office Mojo]] and [[The Numbers (website)|The Numbers]] are both incorrect. Box Office Mojo has been plagued by errors for re-released films since the site was overhauled in 2019, whereby it often double-counts older grosses, as is the case for ''Titanic''. As of 2019, Box Office Mojo correctly recorded that ''Titanic'' had grossed $1.843 billion on its original release, $344 million from its 3D reissue in 2012, and a further $692,000 from a limited release in 2017 for a lifetime total of $2.187 billion.&lt;ref&gt;{{cite web |title=Titanic (1997) |website=[[Box Office Mojo]]  |url=https://www.boxofficemojo.com/title/tt0120338/ |archive-url=https://web.archive.org/web/20191027003338/https://www.boxofficemojo.com/title/tt0120338/ |access-date=October 27, 2019|archive-date=October 27, 2019 }}&lt;/ref&gt; Following a limited re-release in 2020, Box Office Mojo incorrectly added $7 million to the original release total.&lt;ref&gt;{{cite web |title=Titanic (1997) |website=[[Box Office Mojo]]  |url=https://www.boxofficemojo.com/title/tt0120338/ |archive-url=https://web.archive.org/web/20201030074558/https://www.boxofficemojo.com/title/tt0120338/ |access-date=October 30, 2020|archive-date=October 30, 2020 }}&lt;/ref&gt; By the end of 2021, Box Office Mojo had corrected the original release total, but added the $7 million figure to both the 2012 and 2017 reissue totals, incorrectly increasing the lifetime total by $14 million to $2.202 billion.&lt;ref&gt;{{cite web |title=Titanic (1997) |website=[[Box Office Mojo]]  |url=https://www.boxofficemojo.com/title/tt0120338/ |archive-url=https://web.archive.org/web/20211026222823/https://www.boxofficemojo.com/title/tt0120338/ |access-date=October 26, 2021|archive-date=October 26, 2021 }}&lt;/ref&gt; At the beginning of 2023, Box Office Mojo corrected the total for the 2017 reissue, bringing the lifetime gross down $2.195 billion, but retained the error in the 2012 reissue.&lt;ref&gt;{{cite web |title=Titanic (1997) |website=[[Box Office Mojo]]  |url=https://www.boxofficemojo.com/title/tt0120338/ |archive-url=https://web.archive.org/web/20230205001927/https://www.boxofficemojo.com/title/tt0120338/ |access-date=February 28, 2023|archive-date=February 5, 2023 }}&lt;/ref&gt; The Numbers also has an incorrect figure recorded for the lifetime gross. The Numbers does not log individual releases, but had the lifetime total recorded as $2.186 billion in September 2014 (roughly equating to $1.843 billion for the original release and $343.6 million for the 3D reissue).&lt;ref&gt;{{cite web |title=Titanic |website=[[The Numbers (website)|The Numbers]]  |url=http://www.the-numbers.com/movie/Titanic#http://www.the-numbers.com/movie/#tab=summar&amp;tab=summary |archive-url=https://web.archive.org/web/20140902192258/http://www.the-numbers.com/movie/Titanic#http://www.the-numbers.com/movie/#tab=summar&amp;tab=summary |access-date=September 2, 2014|archive-date=September 2, 2014 }}&lt;/ref&gt; A couple of weeks later, The Numbers increased the lifetime gross to $2.208 billion, without explanation.&lt;ref&gt;{{cite web |title=Titanic |website=[[The Numbers (website)|The Numbers]]  |url=http://www.the-numbers.com/movie/Titanic#http://www.the-numbers.com/movie/#tab=summary&amp;tab=summary |archive-url=https://web.archive.org/web/20140913203854/http://www.the-numbers.com/movie/Titanic#http://www.the-numbers.com/movie/#tab=summary&amp;tab=summary |access-date=September 13, 2014|archive-date=September 13, 2014 }}&lt;/ref&gt; Prior to the 2023 re-release, the totals at both trackers were inflated above the true figure. For clarity, ''Titanic'' earned $1.843 billion on its original release, $344 million from its 2012 reissue, $691,642 from the 2017 reissue, and $71,352 in 2020, for a lifetime total of ${{formatnum:{{#expr:1843373318+343550770+691642+71352}}}} from the first four releases. Along with the $70.2 million grossed from the 25th anniversary re-release in 2023,&lt;ref&gt;{{cite web |title=Titanic (25 Year Anniversary) |website=[[Box Office Mojo]] |url=https://www.boxofficemojo.com/releasegroup/gr3800912389/ |access-date=March 21, 2023 |archive-date=March 21, 2023 |archive-url=https://web.archive.org/web/20230321032219/https://www.boxofficemojo.com/releasegroup/gr3800912389/ |url-status=live }}&lt;/ref&gt; the lifetime total for ''Titanic'' stands at ${{formatnum:{{#expr:1843373318+343550770+691642+71352+&lt;!-- 2023 REISSUE --&gt;70157472}}}} {{as of|lc=y|2023|5|22|df=US}}.}}&lt;ref name="BoxOfficeBOM"&gt;*Pre-2020 releases: {{cite web |title=Titanic (1997) |website=[[Box Office Mojo]] |url=https://www.boxofficemojo.com/title/tt0120338/ |archive-url=https://web.archive.org/web/20191027003338/https://www.boxofficemojo.com/title/tt0120338/ |archive-date=October 27, 2019 |quote=Worldwide: $2,187,463,944; Original release: $1,843,221,532; 2012 3D Release: $343,550,770; 2017 Re-release: $691,642 }}
*2020 Re-release: {{cite web |title=Titanic (2020 Re-release) |website=Box Office Mojo |url=https://www.boxofficemojo.com/releasegroup/gr2694926853/ |quote=2020 Re-release: $71,352 |access-date=February 20, 2023 |archive-date=March 5, 2023 |archive-url=https://web.archive.org/web/20230305215849/https://www.boxofficemojo.com/releasegroup/gr2694926853/ |url-status=live }}
*2023 Re-release: {{cite web |title=Titanic (25 Year Anniversary) |website=Box Office Mojo |url=https://www.boxofficemojo.com/releasegroup/gr3800912389/ |quote=2023 Re-release: $70,157,472 |access-date=February 20, 2023 |archive-date=February 27, 2023 |archive-url=https://web.archive.org/web/20230227203751/https://www.boxofficemojo.com/releasegroup/gr3800912389/ |url-status=live }}&lt;/ref&gt;
}}
"""

infobox_dict = extract_infobox(wikitext)
print(infobox_dict)
