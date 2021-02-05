;was siteTable, but want2start kicking out start of: 
;  https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/DataRepository.md
;should redo this in py soon, anyway

;Also have w/py pandas, &could be more fine grain, but this was quick sites2~table script
;df=pd.read_table('cdf_cndls.tsv') print(df[0:18].to_html()) ;mbobak@illinois.edu
;The formatting will change, incl maybe going into a real table, in an about.html page
(defvar *is* " style=\"max-width: 80px; max-height: 40px\" ")
(ql 'cl-csv)
(defvar *csv* (cl-csv:read-csv #P"CDF_Sites.csv"))
(defvar *c1* (first *csv*)) ;headings
(defvar *cf* (rest *csv*))  ;rest of csv
(defvar *c* (subseq *cf* 0 18)) ;was 17
(defvar *c2* (first *c*)) ;for testing
(defun ldns (l &optional (hover t))
  "format:logo domain-name summary"
  (let ((repo (nth 0 l))
        (logo (nth 11 l))
        (domain (nth 7 l))
        (num_datasets (nth 4 l))
        (name (nth 6 l))
        (summary (nth 13 l)))
    ;   (format nil "~%<br><div title=\"~a\"><img ~a src=~a></div><a href=~a>~a</a>" 
    ;           summary *is* logo domain name )
    (if hover
        ;format nil "~%<div title=\"~a\"><a href=~a><img ~a src=~a></div>~a</a>," 
       (format nil 
       "~%<td width=33%><div title=\"~a [~a records]\"><a href=~a><img ~a src=~a></div>~a</a>[~a records]</td>" 
                summary num_datasets domain *is* logo (or name repo) num_datasets)
        (format nil "~%<br><img ~a src=~a><a href=~a>~a</a>,~a" *is* logo
                domain name summary)
    )))
;f_repo = """ f'{
; "@context": {
;   "@vocab": "https://schema.org/"
; },
; "@type": ["Service", "ResearchProject"],
; "legalName": "{name}",
; "name": "{index}",
; "url": "{domain}",
; "description": "{description}.",
; "sameAs": "{re3}"
; }' """
(defun rld (l)
  "repo jsonLD line"
  (let ((index (nth 0 l))
        (name (nth 6 l))
        (domain (nth 7 l))
        (summary (nth 14 l))
        (re3 (nth 13 l))
        )
    (list 
    (format nil "~%~%{  \"@context\": {   \"@vocab\": \"https://schema.org/\"; }, ")
    (format nil "~% \"@type\": [\"Service\", \"ResearchProject\"],")
    (format nil "~% \"legalName\": \"{~a}\"," name)
    (format nil "~% \"name\": \"{~a}\"," index)
    (format nil "~% \"url\": \"{~a}\"," domain)
    (format nil "~% \"description\": \"{~a}\"," summary)
    (format nil "~% \"sameAs\": \"{~a}\"}" re3)
    )))

;-
(defun pt (lol)
  "print table"
  (mapcar #'ldns lol))

(defun tp (&optional (lol *c*))
  "test print"
  (pt lol))

(defun stc (&optional (fn "c3.htm"))
  "save(test)table"
  (save-lines (tp) fn))

;-
(defun pr (lol)
  "print repo"
  (mapcar #'rld lol))

(defun tr (&optional (lol *c*))
  "test print repo"
  (pr lol))

(defun str (&optional (fn "repo.jsonld"))
  "save(test)repo"
  (save-lines (flatten1 (tr)) fn))
