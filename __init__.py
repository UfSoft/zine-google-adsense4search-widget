# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: __init__.py 96 2008-02-27 14:29:06Z s0undt3ch $
# =============================================================================
#             $URL: http://devnull.ufsoft.org/svn/GoogleAdsenseForSearchWidget/trunk/__init__.py $
# $LastChangedDate: 2008-02-27 14:29:06 +0000 (Wed, 27 Feb 2008) $
#             $Rev: 96 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2007 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================
# https://www.google.com/support/googleanalytics/bin/answer.py?answer=55585&topic=10981

from os.path import join, dirname
from textpress.widgets import Widget
from textpress.api import *

#SHARED_FILES = join(dirname(__file__), 'shared')
TEMPLATES = join(dirname(__file__), 'templates')

class GoogleAdsenseForSearchWidget(Widget):
    __metaclass__ = cache.make_metaclass(vary=('user',))
    NAME = 'get_google_search_box'
    TEMPLATE = 'google_search_widget.html'

    def __init__(self, show_title=False, sbi='Enter your search terms',
                 ss0_label='Search the Web', ss1_label='Search',
                 sbb_label='Submit search form', submit_button_value='Search',
                 client='', forid='', channel='', safe_contents=True,
                 background='white', cof='', hl='',
                 site_domain='', google_search_domain='www.google.com',
                 google_gif='Logo_25wht.gif', font_colour='#000000',
                 bg_colour='#ffffff', input_field_size='31'):
        self.show_title = show_title
        self.sbi = sbi
        self.ss0_label = ss0_label
        self.ss1_label = ss1_label
        self.sbb_label = sbb_label
        self.submit_button_value = submit_button_value
        self.client = client
        self.forid = forid
        self.channel = channel
        self.safe_contents = safe_contents
        self.background = background
        self.cof = cof
        self.hl = hl
        self.site_domain = site_domain
        self.google_search_domain = google_search_domain
        self.google_gif = google_gif
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.input_field_size = input_field_size

#        self.TEMPLATE = "google_search_widget_%s.html" % background

    @staticmethod
    def get_display_name():
        return _('Google Adsense For Search')

    @staticmethod
    def configure_widget(initial_args, request):
        args = form = initial_args.copy()
        errors = []
        if 'site_domain' not in initial_args:
            args['site_domain'] = request.environ.get('HTTP_HOST')

        if request.method == 'POST':
            args['sbi'] = request.form.get('sbi')
            if not args['sbi']:
                errors.append(_("SBI must be set."))
            args['ss0_label'] = request.form.get('ss0_label')
            if not args['ss0_label']:
                errors.append(_("SS0 Label must be set."))
            args['ss1_label'] = request.form.get('ss1_label')
            if not args['ss1_label']:
                errors.append(_("SS1 Label must be set."))
            args['sbb_label'] = request.form.get('sbb_label')
            if not args['sbb_label']:
                errors.append(_("SSB Label must be set."))
            args['submit_button_value'] = request.form.get('submit_button_value')
            if not args['submit_button_value']:
                errors.append(_("Submit Button Value must be set."))
            args['client'] = request.form.get('client')
            if not args['client']:
                errors.append(_("Client ID must be set."))
            args['forid'] = request.form.get('forid')
            if not args['forid']:
                errors.append(_("Forid must be set."))
            args['channel'] = request.form.get('channel')
            args['safe_contents'] = request.form.get('safe_contents') == 'yes'
            args['background'] = background = request.form.get('background')
            if background == 'white':
                args['font_colour'] = '#000000'
                args['bg_colour'] = '#ffffff'
                args['google_gif'] = 'Logo_25wht.gif'
            elif background == 'black':
                args['font_colour'] = '#ffffff'
                args['bg_colour'] = '#000000'
                args['google_gif'] = 'Logo_25blk.gif'
            elif background == 'grey':
                args['font_colour'] = '#000000'
                args['bg_colour'] = '#cccccc'
                args['google_gif'] = 'Logo_25gry.gif'
            else:
                errors.append(_("Background must be one of 'white', 'black', "
                                "'grey'."))
            args['input_field_size'] = request.form.get('input_field_size', '31')
            args['cof'] = request.form.get('cof')
            if not args['cof']:
                errors.append(_("COF must be set."))
            args['hl'] = request.form.get('hl')
            if not args['hl']:
                errors.append(_("HL must be set."))
            args['site_domain'] = request.form.get('site_domain')
            if not args['site_domain']:
                errors.append(_("Site Domain must be set."))
            args['google_search_domain'] = google_search_domain = \
                request.form.get('google_search_domain')
            if not google_search_domain:
                errors.append(_("Google Search Domain must be set."))
            else:
                request.app.cfg[
                    'google_adsense_for_search/google_search_domain'
                ] = google_search_domain

        if errors:
            args = None
        return args, render_template('admin/google_search_widget.html',
                                     errors=errors, form=form,
                                     site_domain=request.environ['HTTP_HOST'])


def do_search_results(req):
    options = {}
    options['google_search_domain'] = \
        req.app.cfg['google_adsense_for_search/google_search_domain'].\
		    encode('utf-8')
    return render_response('google_search_results.html', **options)

def setup(app, plugin):
    app.add_config_var('google_adsense_for_search/google_search_domain',
                       unicode, u'www.google.com')
    #app.add_shared_exports('google_adsense_for_search', SHARED_FILES)
    app.add_template_searchpath(TEMPLATES)
    app.add_widget(GoogleAdsenseForSearchWidget)
    app.add_url_rule('/search', view=do_search_results,
                     endpoint='google_search/results')

