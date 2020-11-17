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
  (rest (first-lv
    (decode-json-from-str
     (dex:get (strcat *clowder-host* "/api/datasets/" id "/metadata.jsonld"))))))

(defun LDelts (id el)
  "elt-list from LD"
  (let ((ld (getLD id)))
    (mapcar #'(lambda (e) (assoc-v e ld)) el))) 

(defun id (ds) "get ID from dataset alst" (assoc-v :ID ds))
(defun ldc (ld) "get  CONTENT from LD alst" (rest-lv (assoc-v :CONTENT ld)))
(defun url (ld) "get publisher from LD alst" (assoc-v :URL ld))
(defun name (ld) "get publisher from LD alst" (assoc-v :NAME ld))
(defun pub (ld) "get publisher from LD alst" (assoc-v :PUBLISHER ld))
(defun get-pub (al)
  "get publisher"
  (let ((publ (assoc-v :PUBLISHER al)))
    (if (listp publ) (assoc-v :NAME (rest-lv (first-lv (first-lv publ))))
      publ)))
;(trace get-pub) 
(defun results (ds) (assoc-v :RESULTS ds))

(defun phit (ds)
  "print just1of the search results"
  (let* ((id (id ds))
         (ld  (getLD id))
         (ldc (ldc ld))
         (ln (len ldc))
         ;(pub (pub ld))
         ;(url (url ld))
         ;(url2 (url ldc))
         ;;(m3 (mapcar #'(lambda (e) (assoc-v e ld))  '(:NAME :PUBLISHER :URL)))
         ;(m3 (mapcar #'(lambda (e) (cons e (assoc-v e ldc))) '(:NAME :PUBLISHER :URL)))
         (m3 (mapcar #'(lambda (ef) (cons e (funcall ef ldc))) '(#'name #'get-pub #'url)))
         )
    (print (str-cat "==================id= " id ",len=" ln ",url=" m3))
    (print ld)
    (print "------------------------------------------------------------------------------")
    m3))

(defun qry2 (str)
  (let* ((ql (qry str))
         (res (results ql)))
    (mapcar #'phit res)))

;can more quickly play w/sca.py search return values, to construct the correct results
; btw, might collect distict filter/facet values&get counts, for things like publishers..
(defun tq ()
  "test qry"
  (qry2 "multibeam sonar"))
;(((:NAME . "NOAA TIFF Image - 50m Backscatter, Charleston Bump - Deep Coral Priority Areas - Nancy Foster - (2006), UTM 17N NAD83NOAA/NMFS/EDM")
; (:PUBLISHER . "publisher not specified") (:URL))
;((:NAME . "Gridded backscatter mosaic of Venere mud volcano (MV), based on AUV MARUM-SEAL data acquisition during POS499")
; (:PUBLISHER
;  ((:|| (:@TYPE . "Organization")
;    (:NAME . "PANGAEA - Data Publisher for Earth & Environmental Science"))
;   (:@TYPE . "Role") (:ROLE-NAME . "publisher")))
; (:URL))
;((:NAME . "AWI Bathymetric Chart of the Fram Strait (BCFS) (Scale 1:100,000)")
; (:PUBLISHER
;  ((:|| (:@TYPE . "Organization")
;    (:NAME . "PANGAEA - Data Publisher for Earth & Environmental Science"))
;   (:@TYPE . "Role") (:ROLE-NAME . "publisher")))
; (:URL))
;((:NAME . "NOAA TIFF Image - 4m Bathymetric Mean Depth of Red Snapper Research Areas in the South Atlantic Bight, 2010NOAA/NMFS/EDM")
; (:PUBLISHER . "publisher not specified") (:URL))
;((:NAME
;  . "NOAA TIFF Image - 50m Multibeam Bathymetry, Charleston Bump - Deep Coral Priority Areas - Little Hales - (2003), UTM 17N NAD83NOAA/NMFS/EDM")
; (:PUBLISHER . "publisher not specified") (:URL))
;((:NAME
;  . "NOAA TIFF Image - 10m Multibeam Bathymetry, South Atlantic Bight - Deep Coral Priority Areas - NOAA Ship Nancy Foster - (2009), UTM 17N NAD83NOAA/NMFS/EDM")
; (:PUBLISHER . "publisher not specified") (:URL)))

;cleans up the getting of publisher
;(print (mapcar #'get-pub *ret*)) ;where *ret* is what is comments just above
;("publisher not specified"
 ;"PANGAEA - Data Publisher for Earth & Environmental Science"
 ;"publisher not specified" "publisher not specified" "publisher not specified"
 ;"PANGAEA - Data Publisher for Earth & Environmental Science")
