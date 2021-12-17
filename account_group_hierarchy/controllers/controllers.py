# -*- coding: utf-8 -*-
from odoo import http


class AddsonAccountParent(http.Controller):
    @http.route('/addson/account_parent/addson/account_parent/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/addson/account_parent/addson/account_parent/objects/', auth='public')
    def list(self, **kw):
        print("----------- call list ============")
        return http.request.render('addson/account_parent.listing', {
            'root': '/addson/account_parent/addson/account_parent',
            'objects': http.request.env['addson/account_parent.addson/account_parent'].search([]),
        })

    @http.route('/addson/account_parent/addson/account_parent/objects/<model("addson/account_parent.addson/account_parent"):obj>/', auth='public')
    def object(self, obj, **kw):
        print(".................call object ..............")
        return http.request.render('addson/account_parent.object', {
            'object': obj
        })
