(defun split-by-colon (s)
  (when (len-gt s 2)
      (explode- s #\:)))

;defun s-parse-number (n)
  ;when (numberp

(defun colon-num (s)
  "split-by-colon where 2nd is a number"
  (let* ((l (split-by-colon s))
         (l2 (second l)))
    (when (len-gt l2 0)
        (setf (second l) (s2num l2)))
    l))

(defvar *repos* '("balto" "bco-dmo" "earthchem" "edi" "hydroshare" "iedadata" "iris" "magic" "neotomadb" "opencoredata" "opentopography" "rr" "ssdb.iodp" "ucar" "unavco"))

;(defvar *qryb*  "hydrologic|extremes")
;the starting fnc should take this as a space delimited, trim edges, replace middle-spaces w/'|'
;then call the rest of this ;might also give, max#to return, eg. 1k 
;w/ability of  a min+cutoff eg. >1hit, but w/at least 500 returned
(ql 'cl-ppcre)
(defun space2bar (s)
  ;(simple-replace-string " " "|" s)
  (cl-ppcre:regex-replace-all " " s "|")
  )
(defvar *qryb*  (space2bar "hydrologic extremes"))

(defun matchesInRepo (repo) 
    ;cs=f"ag -c '{qryb}' {repo}/*.jsonld"
    ;mapcar #'split-by-colon
    (mapcar #'colon-num
        (break2lines (tsh (strcat "ag -c '" *qryb* "' " repo "/*.jsonld")))))

(defun matches (&optional (rl *repos*))
  (sort (rm-nils (flat1 (mapcar #'matchesInRepo rl)))
        #'> :key #'second-lv))

(defvar *m* (matches))
;USER(1): (len *m*) 
;1427
;USER(2): (head *m*)
;(("hydroshare/f16c8715b349b78d0a3c6ebd2c0eb450d99649ac.jsonld" 18)
; ("hydroshare/64f586d7d3bcfaea0ea3442c38d32238aacc5d84.jsonld" 13)
; ("hydroshare/139af606f0e0636e5624df79c10a72ce36080012.jsonld" 12)
; ("hydroshare/dbd8ef5ef650d987f3b8cc7f655f5e6cf8409e53.jsonld" 11))
;USER(3): (tail *m*)
;(("ucar/variation-of-atmospheric-co-c-and-o-at-high-northern-latitude-during-2004-2009-observations-and.jsonld" 1)
; ("ucar/volcanic-eruption-signatures-in-the-isotopeenabled-last-millennium-ensemble.jsonld" 1)
; ("ucar/warming-and-human-activities-induced-changes-in-the-yarlung-tsangpo-basin-of-the-tibetan-platea.jsonld" 1)
; ("ucar/zooplankton-abundance-and-biomass-retrospective.jsonld" 1))
;USER(4): 
;try out idea:
; of having a ranked search, ret a list of jsonLD for a TriplePatterFragrment like search after
;Did this on jsonLD, but could have done on .nt files, &started to load them in a store of sorts
 ;in fact this could be done on the clients side; esp.if reduced in size
  ;cmp this w/the traffice /&time that is taken now
;also having the triples on the clients could make for some interesing posabilities there
