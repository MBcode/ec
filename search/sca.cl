;need to move fast in getting elts out of jsonLD
(defvar *clowder-host* "https://earthcube.clowderframework.org")
(ql 'dexador) ;github.com/fukamachi/dexador
(ql 'drakma)
(defun safe-url (u)
  (drakma:url-encode u :utf-8))

;from js.cl
(require :cl-json)
;(defun encode-json2str (js) (json:encode-json-to-string js))
(defun encode-json2str (js)
  (if (equal js '(nil)) "[]"
    (json:encode-json-to-string js)))
;(defun decode-json-from-str (str) (json:decode-json-from-string str))
(defun decode-json-from-str (str)
  (if (equal "[]" str) '(nil)
    (json:decode-json-from-string str)))
;

;lets redo some of the NB 1st
(defun qry (str)
  (let ((qry_str (safe-url str)))
    (decode-json-from-str
     (dex:get (strcat *clowder-host* "/api/search?query=" qry_str)))))

(defun getLD (id)
    (decode-json-from-str
     (dex:get (strcat *clowder-host* "/api/datasets/" id "/metadata.jsonld"))))

(defun id (ds)
  "get ID from dataset alst"
  (assoc-v :ID ds))

(defun results (ds) (assoc-v :RESULTS ds))

(defun phit (ds)
  "print just1of the search results"
  (let ((id (id ds))
        (ln (len ds))
       ;(ln  ds)
        )
    (print (str-cat "id= " id ",len=" ln))))

(defun qry2 (str)
  (let* ((ql (qry str))
         (res (results ql)))
    (mapcar #'phit res)))

(defun tq ()
  "test qry"
  (qry2 "multibeam sonar"))
;("id= 5f829e1fe4b0b81250e2e12d,len=8" "id= 5f8278e5e4b0b81250da8c9a,len=8"
;"id= 5f82794be4b0b81250dab844,len=8" "id= 5f8294b9e4b0b81250e26dd2,len=8"
;"id= 5f829fb1e4b0b81250e2f4af,len=8" "id= 5f829f48e4b0b81250e2ef95,len=8")
;can more quickly play w/sca.py search return values, to construct the correct results
; btw, might collect distict filter/facet values&get counts, for things like publishers..
