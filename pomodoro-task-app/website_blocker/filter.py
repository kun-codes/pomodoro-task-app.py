# Copyright: (c) 2018, Aniket Panjwani <aniket@addictedto.tech>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Filter URLs according to rules."""

import os
import sys

# append directory containing constants.py to path so that BLOCK_HTML_MESSAGE can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants import BLOCK_HTML_MESSAGE
from mitmproxy import ctx, http


def load(l):
    l.add_option("addresses_str", str, "", "Concatenated addresses.")
    l.add_option("block_type", str, "", "Whitelist or blacklist.")


def request(flow):
    addresses = ctx.options.addresses_str.split(",")
    addresses = set(addresses)

    addresses = {address for address in addresses if address}

    has_match = any(address in flow.request.pretty_url for address in addresses)
    if ctx.options.block_type == "allowlist" and not has_match or ctx.options.block_type == "blocklist" and has_match:
        flow.response = http.Response.make(200, BLOCK_HTML_MESSAGE.encode(), {"Content-Type": "text/html"})
