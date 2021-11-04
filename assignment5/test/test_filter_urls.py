from filter_urls import find_urls


def test_find_urls():
    html = """
    <a href="#fragment-only">anchor link</a>
    <a id="some-id" href="/relative/path#fragment">relative link</a>
    <a href="//other.host/same-protocol">same-protocol link</a>
    <a href="https://example.com">absolute URL</a>
    """
    urls = find_urls(html, base_url="https://en.wikipedia.org")
    assert urls == [
        "https://en.wikipedia.org/relative/path",
        "https://other.host/same-protocol",
        "https://example.com",
        ]

    test_page = """<html class="client-js ve-available" lang="en" dir="ltr"><head><body class="mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-Pausanias_of_Athens rootpage-Pausanias_of_Athens skin-vector action-view skin-vector-legacy" data-new-gr-c-s-check-loaded="14.1036.0" data-gr-ext-installed=""><div id="mw-page-base" class="noprint"></div>
<div id="mw-head-base" class="noprint"></div>
<div id="content" class="mw-body" role="main">
	<a id="top"></a>
	<div id="siteNotice"><div id="centralNotice"></div><!-- CentralNotice --></div>
	<div class="mw-indicators">
	</div>
	<h1 id="firstHeading" class="firstHeading">Pausanias of Athens</h1>
	<div id="bodyContent" class="vector-body">
		<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>
		<div id="contentSub"></div>
		<div id="contentSub2"></div>
		
		<div id="jump-to-nav"></div>
		<a class="mw-jump-link" href="#mw-head">Jump to navigation</a>
		<a class="mw-jump-link" href="#searchInput">Jump to search</a>
		<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><p><b>Pausanias</b> (<span class="rt-commentedText nowrap"><span class="IPA nopopups noexcerpt"><a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="'p' in 'pie'">p</span><span title="/ɔː/: 'au' in 'fraud'">ɔː</span><span title="/ˈ/: primary stress follows">ˈ</span><span title="'s' in 'sigh'">s</span><span title="/eɪ/: 'a' in 'face'">eɪ</span><span title="'n' in 'nigh'">n</span><span title="/i/: 'y' in 'happy'">i</span><span title="/ə/: 'a' in 'about'">ə</span><span title="'s' in 'sigh'">s</span></span>/</a></span></span>; <a href="/wiki/Greek_language" title="Greek language">Greek</a>: <span lang="grc" title="Ancient Greek (to 1453)-language text">Παυσανίας</span>; fl. c. 420 BC) was an <a href="/wiki/Classical_Athens" title="Classical Athens">ancient Athenian</a> of the <a href="/wiki/Deme" title="Deme">deme</a> <a href="/wiki/Cerameis" title="Cerameis">Kerameis</a>, who was the lover of the poet <a href="/wiki/Agathon" title="Agathon">Agathon</a>.
</p><p>Although Pausanias is given a significant speaking part in <a href="/wiki/Plato" title="Plato">Plato</a>'s <i><a href="/wiki/Symposium_(Plato)" title="Symposium (Plato)">Symposium</a></i>, very little is known about him.  Ancient anecdotes tend to address only his relationship with Agathon and give us no information about his personal accomplishments.  Around 407 BC he removed himself from Athens to the court of the Macedonian king <a href="/wiki/Archelaus_I_of_Macedon" title="Archelaus I of Macedon">Archelaus</a>."""

    urls = find_urls(test_page, base_url="")
    results = ["/wiki/Help:IPA/English", "/wiki/Greek_language", "/wiki/Classical_Athens",
               "/wiki/Deme", "/wiki/Cerameis", "/wiki/Agathon", "/wiki/Plato",
               "/wiki/Symposium_(Plato)", "/wiki/Archelaus_I_of_Macedon"]
    
    assert urls == results
