(require 'package)
(add-to-list 'package-archives '("melpa"
				 . "https://melpa.org/packages/"))
(package-refresh-contents)
(package-initialize)

(unless (package-installed-p 'use-package) (package-install
					    'use-package))
(require 'use-package)
;; Python
(use-package lsp-pyright
  :ensure t
  :hook (python-mode . (lambda ()
			 (require 'lsp-pyright)
			 (lsp))))
;; Haskell
(unless (package-installed-p 'haskell-mode) (package-install
					     'haskell-mode))
;; Themes
(use-package doom-themes
  :ensure t
  :config
  (setq doom-themes-enable-bold t    ; if nil, bold is universally disabled
        doom-themes-enable-italic t) ; if nil, italics is universally disabled
  (load-theme 'doom-one t))
