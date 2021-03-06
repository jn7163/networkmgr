#!/usr/local/bin/python

import gtk
from net_api import scanWifiBssid, connectToSsid

wpa_supplican = "/etc/wpa_supplicant.conf"


class Authentication:
    def button(self):
        cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        cancel.connect("clicked", self.close)
        connect = gtk.Button(stock=gtk.STOCK_CONNECT)
        connect.connect("clicked", self.add_to_wpa_supplicant)
        table = gtk.Table(1, 2, True)
        table.set_col_spacings(10)
        table.attach(connect, 4, 5, 0, 1)
        table.attach(cancel, 3, 4, 0, 1)
        return table

    def close(self, widget):
        self.window.hide()

    def add_to_wpa_supplicant(self, widget):
        pwd = self.password.get_text()
        Look_Wpa_Supplicant(self.ssid, self.bssid, pwd)
        self.window.hide()

    def on_check(self, widget):
        if widget.get_active():
            self.password.set_visibility(True)
        else:
            self.password.set_visibility(False)

    def __init__(self, ssid, bssid):
        self.ssid = ssid
        self.bssid = bssid
        self.window = gtk.Window()
        self.window.set_title("wi-Fi Network Authetification Required")
        self.window.set_border_width(0)
        # self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500, 200)
        # self.window.set_icon_from_file("/usr/local/etc/gbi/logo.png")
        box1 = gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Creating MBR or GPT drive
        title = "Authetification required by %s Wi-Fi Network" % ssid
        label = gtk.Label("<b><span size='large'>%s</span></b>" % title)
        label.set_use_markup(True)
        pwd_label = gtk.Label("Password:")
        self.password = gtk.Entry()
        self.password.set_visibility(False)
        check = gtk.CheckButton("Show password")
        check.connect("toggled", self.on_check)
        table = gtk.Table(1, 2, True)
        table.attach(label, 0, 5, 0, 1)
        table.attach(pwd_label, 1, 2, 2, 3)
        table.attach(self.password, 2, 4, 2, 3)
        table.attach(check, 2, 4, 3, 4)
        box2.pack_start(table, False, False, 0)
        box2 = gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add create_scheme button
        box2.pack_end(self.button(), True, True, 5)
        self.window.show_all()


class Open_Wpa_Supplicant:
    def __init__(self, ssid, bssid):
        ws = '\nnetwork={'
        ws += '\n\tssid="%s"' % ssid
        ws += '\n\tbssid=%s' % bssid
        ws += '\n\tkey_mgmt=NONE\n}'
        wsf = open(wpa_supplican, 'a')
        wsf.writelines(ws)
        wsf.close()
        connectToSsid(ssid)


class Look_Wpa_Supplicant:
    def __init__(self, ssid, bssid, pwd):
        if 'RSN' in scanWifiBssid(bssid):
            # /etc/wpa_supplicant.conf written by networkmgr
            ws = '\nnetwork={'
            ws += '\n\tssid="%s"' % ssid
            ws += '\n\tbssid=%s' % bssid
            ws += '\n\tkey_mgmt=WPA-PSK'
            ws += '\n\tproto=RSN'
            ws += '\n\tpsk="%s"\n}\n' % pwd
        elif 'WPA' in scanWifiBssid(bssid):
            ws = '\nnetwork={'
            ws += '\n\tssid="%s"' % ssid
            ws += '\n\tbssid=%s' % bssid
            ws += '\n\tkey_mgmt=WPA-PSK'
            ws += '\n\tproto=WPA'
            ws += '\n\tpsk="%s"\n}\n' % pwd
        else:
            ws = '\nnetwork={'
            ws += '\n\tssid="%s"' % ssid
            ws += '\n\tbssid=%s' % bssid
            ws += '\n\tkey_mgmt=NONE'
            ws += '\n\twep_tx_keyidx=0'
            ws += '\n\twep_key0=%s\n}\n' % pwd
        wsf = open(wpa_supplican, 'a')
        wsf.writelines(ws)
        wsf.close()
        connectToSsid(ssid)
