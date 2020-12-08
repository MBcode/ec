#!/home/bobak/anaconda3/bin/hy
(print (first ["hi" "there"]))
(import requests)
(import json)
(import [json [dumps]]) ;probably can list out together
(import [json [loads]])
(import [pprint [pprint]])
(require [hy.contrib.walk [let]])
(import os)
(setv clowder_host (os.environ.get "clowder_host"))
;(setv clowder_host "https://earthcube.clowderframework.org")
(print clowder_host)
(defn cid2ld [cid]
     ;(requests.get f'{clowder_host}/api/datasets/{cid}/metadata.jsonld')
     (setv response (requests.get (+ clowder_host "/api/datasets/" cid "/metadata.jsonld")))
     (first ;json.json
      (response.json) ;(requests.get (+ clowder_host "/api/datasets/" cid "/metadata.jsonld"))
      ))

(defn save-txt2file [txt fn]
      (with [f (open fn "w")] (.write f txt)))

(defn get-txtfile [fn]
      (with [f (open fn "r")] (.read f)))

;(defn get-jsonfile [fn]
;      (with [f (open fn)] (json.loads f)))
(defn get-jsonfile [fn]
      ;json.loads 
      (loads 
        (get-txtfile fn)))

(defn cid2ld_ [cID]
      (let [ccf (+ "cc/" cID ".jsonld")]
        (if (os.path.exists ccf)  (get-jsonfile ccf)
          (let [nd (cid2ld cID)]
            ;(save-txt2file nd ccf)
            (save-txt2file 
              (dumps nd) 
              ccf)
            nd))))

(defn gd [id]
      (cid2ld_ id))
(defn td []
      (pprint (gd "5f82911ae4b0b81250e2419d")))
(td)
