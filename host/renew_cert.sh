#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

# Renews the HTTPS certification via certbot

certbot renew --nginx
systemctl reload nginx
