# SPDX-FileCopyrightText: 2022 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

.PHONY: roles lint

help: ## Show this help.
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\\$$//' | sed -e 's/##//'

roles: ## Pull roles
	rm -rf roles/galaxy
	ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force

lint: ## Runs ansible-lint against all roles in the playbook
	ansible-lint roles/custom
