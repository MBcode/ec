;#====read sitemap.xml into *l1* format
(ql 's-xml)
(defun file2xml (fn)
  (s-xml:parse-xml-string (file2string fn)))
;(load "l1.l" :print t)
(defvar *x* (file2xml "sitemap.xml"))
(defun xurl (l) (second-lv (second-lv l)))
(defvar *x2* (mapcar #'xurl (rest *x*)))
(defun url-parts (url)
  (explode-str url :sep #\/))
(defun last-url-part (url)
    (last_lv (url-parts url))) 
(defun after= (s)
  (second-lv (split-string s #\=))) ;second_lv might ..
(defun last-url-part-after= (url)
  (after= (first-lv (last-url-part url))))
(defvar *l1*  
 (mapcar #'last-url-part *x2*)
 ;(mapcar #'last-url-part-after= *x2*) ;for opentopography
  )
;======see how much of sitemap has gone to js/jsonld /nt, so can finish off new ones
;parse sitemap above, instead of:
;(load "l1.l" :print t) ;has the base/max# from sitemap
(defun rm-jsonld (s) (rm-str s ".jsonld"))
;just use rm-ext
(defvar *js* (mapcar #'rm-ext (ls "js")))
(defvar *ld* (mapcar #'rm-ext (ls "ld")))
(defvar *nt* (mapcar #'rm-ext (ls "nt")))
(defvar *ln* (mapcar #'length (list *js* *ld* *nt* *l1*)))
(print *ln*)
(defvar *js2* (set-difference *l1* *js*  :test 'equal))
(defvar *ld2* (set-difference *l1* *ld*  :test 'equal))
(defvar *nt2* (set-difference *l1* *nt*  :test 'equal))
(defvar *ln2* (mapcar #'length (list *js2* *ld2* *nt2*)))
(print *ln2*)
(defun lenlgt (l &optional (gt 99)) 
  "len and list if > gt"
  (let ((ln (len l)))
    (if (> ln gt) ln
      (list ln l))))
;(format t "~%js2do:~a" (len *js2*))
;(format t "~%js2do:~a"  *js2*)
(format t "~%js2do:~a"  (lenlgt *js2* 199))
;(format t "~%ld2do:~a" (len *ld2*))
;(format t "~%ld2do:~a"  *ld2*)
(format t "~%ld2do:~a"  (lenlgt *ld2* 199))
(format t "~%nt2do:~a" (len *nt2*))
(format t "~%nt2do:~a" *nt2*)
(defun ld2nt (fb)
  (tsh (str-cat "riot ld/" fb ".jsonld |cat>nt/" fb ".nt")))
;might have to finish js2jsonld or just crawl that way now
(defun finish_ld2nt (&optional (td *nt2*))
    (mapcar #'ld2nt td))
;==
;might have to extruct/crawl more
(defvar *base_url* (getenv "BASE_URL")) ;use one that already has =/etc if need be
(defun extbu_ (fb) ;fb2ld
  (tsh (str-cat "extruct " *base_url* fb " --syntaxes json-ld >& " fb ".jsonld")))
(defun finish_fb2ld (&optional (td *ld2*))
    (mapcar #'extbu_ td))
