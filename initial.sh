#!/usr/bin/env bash
createdb tele_order;
psql -c "create user tele_order with password 'tele_order'";
psql -c 'grant all privileges on database tele_order to tele_order';