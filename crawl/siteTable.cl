;was siteTable, but want2start kicking out start of: 
;  https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/DataRepository.md
;should redo this in py soon, anyway

;Also have w/py pandas, &could be more fine grain, but this was quick sites2~table script
;df=pd.read_table('cdf_cndls.tsv') print(df[0:18].to_html()) ;mbobak@illinois.edu
;The formatting will change, incl maybe going into a real table, in an about.html page
;--util add :if-exists :overwrite
(defun save-lineS (l filename)
 (when (fulll l)
  (with-open-file (stream filename :direction :output :if-exists :overwrite)
    (mapcar #'(lambda (x) (write-line x stream)) l))))
;
(defvar *is* " style=\"max-width: 80px; max-height: 40px\" ")
(ql 'cl-csv)
(defvar *csv* (cl-csv:read-csv #P"CDF_Sites.csv"))
(defvar *c1* (first *csv*)) ;headings
(defvar *cf* (rest *csv*))  ;rest of csv
;(defvar *c* (subseq *cf* 0 18)) ;was 17
(defvar *c* (subseq *cf* 0 23)) ;was 17
(defvar *c2* (first *c*)) ;for testing
(defvar *c5* (fourth *c*)) ;for testing
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
       (format nil  ;check divs in final
       "~%<td width=33%><div title=\"~a [~a records]\"><a href=~a><img ~a src=~a></div>~a</a><small>[~a records]</small></td>" 
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
;could just have an ordered list of slotnames, w/something to skip a few
 ;also in py rewrite, import csv, which allows for ref cols by name
(defun rld (l &optional (perRepo nil)) 
  "repo jsonLD line"
  (let ((index (nth 0 l))
        (name (nth 10 l))
        (domain (nth 11 l))
        (summary (nth 17 l))
        ;(re3 (nth 18 l))
        (ror (nth 1 l))
        (re3 (nth 2 l))
        (scholia (nth 3 l))
        (wikidata (nth 4 l))
        (sitemap (nth 5 l))
        (base_url (nth 6 l))
       ;(logo (nth 11 l)) ;will use local version of each, to avoid x http/s problems
        );SoS has logo, get contactPoint&funder too 
    ;https://github.com/ESIPFed/science-on-schema.org/blob/master/examples/data-repository/minimal.jsonld
    (let ((rl (list 
        (format nil "{  \"@context\": {   \"@vocab\": \"https://schema.org/\" }, ")
        (format nil " \"@id\": \"~a\"," domain)
        (format nil " \"@type\": [\"Service\", \"ResearchProject\"],")
        (format nil " \"legalName\": \"~a\"," name)
        (format nil " \"name\": \"~a\"," index)
        (format nil " \"url\": \"~a\"," domain)
        (format nil " \"description\": \"~a\"," summary)
       ;(format nil " \"logo\": { \"@type\": \"ImageObject\", \"url\": \"~a\" }," logo) ;go local:
        (format nil " \"logo\": { \"@type\": \"ImageObject\", \"url\": \"images/repo/~a.png\" }," index)
     ;  (format nil " \"identifier\": \"~a\"}" re3) ;was sameAs
        (format nil " \"ror\": \"~a\"," ror) 
        (format nil " \"re3data\": \"~a\"," re3) 
        (format nil " \"scholia\": \"~a\"," scholia) 
        (format nil " \"wikidata\": \"~a\"," wikidata) 
        (format nil " \"sitemap\": \"~a\"," sitemap) 
        (format nil " \"base_url\": \"~a\"}" base_url) 
        )))
      (if perRepo (cons index rl)
        rl)))) 

(defun repo-ld (l)
  (let* ((idx-ld (rld l t)) 
         (idx (first idx-ld))
         (ld (rest idx-ld))
         (fnt (str-cat "ld/" idx "/repo.nt"))
         (fn (str-cat "ld/" idx "/repo.jsonld")))
  (save-lineS ld fn)
  (tsh (str-cat "riot " fn " |cat> " fnt))
  ))

;-
(defun pt (lol)
  "print table"
  (mapcar #'ldns lol))

(defun tp (&optional (lol *c*))
  "test print"
  (pt lol))

(defun stc (&optional (fn "c3.htm"))
  "save(test)table"
  (save-lineS (tp) fn))

;-
(defun pr (lol)
  "print repo"
  (mapcar #'rld lol)) 

(defun tr (&optional (lol *c*))
  "test print repo"
  (pr lol))

(defun str (&optional (fn "repo.jsonld"))
  "save(test)repo"
  (save-lineS (flatten1 (tr)) fn))

(defun ld-repo (&optional (lol *c*))
  (mapcar #'repo-ld lol))

