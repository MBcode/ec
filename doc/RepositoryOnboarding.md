This will need to be a document to onboard repositories and communities.

Here was [funded project onboarding](https://docs.google.com/document/d/1aNZnWOBdDwZK6KOLf6Zu68QP9RgM3Nakxxf0sA7FhUw/edit) doc:

[Onboarding](https://docs.google.com/document/d/1hk5Y1lspB5qTVQ0rr20YEetoUhvenE2XSRudtZ-NXwY/edit#heading=h.c31noq2qy7rx) for previous office: 

[Archetypes from GleanerIO](https://github.com/gleanerio/archetype) You are a community, or a publisher… here are some tools

[Schema.org paper](https://www.inderscienceonline.com/doi/10.1504/IJBDM.2022.128449) “Schema.org for research data managers: a primer”

Ocean Sciences Best Practice: <https://github.com/adamml/ocean-best-practices-on-schema>

Instead of getting org info in parts, make sure they have a [re3data.org](https://www.re3data.org/)/[suggest](https://www.re3data.org/suggest) ror.org/[request](https://docs.google.com/forms/d/e/1FAIpQLSdJYaMTCwS7muuTa-B_CnAtCSkKzt19lkirAKG4u7umH9Nosg/viewform) .. 

Early sketch of a decision-tree: [github.com/earthcube/ec/doc/onboarding.md](https://github.com/earthcube/ec/blob/master/doc/onboarding.md) 


## Thoughts:

Section 1:

What does [GeoCODES](https://www.earthcube.org/geocodes)/[DeCODER](https://www.earthcube.org/decoder) do?

Section 2:

What we need from you to start

What do we need to help assess you data

What do we need to help assess you Schema.org Dataset Metadata

What we expect once we start

Evaluating your data

Section 3

What will we try to do to ‘qualify’ your information

Sessions:

Some thoughts on how this might work

- Initial contact
- Initial support of development of schema and making data available. 
- Initial loading and review of science on schema
- Moving community to production system

We need some editable location to store the information. A google sheet with a few tabs \[Who are we, Our data, Our Science on schema, Your Data in Geocodes], Template document, 

Section 1:

WHAT THE HELL DOES GEOCODES DO!!!! IN SIMPLE LANGUAGE.SIMPLE. Non Techy. One or two paragraphs. Why would anyone work with us? Wordsmithing this will be a kenton/luigi/christina task. But initially this is a tech team member task. 


### Section 2:


#### What we need from the start,

If they have an identifier, then in future we can pull _some_ information from that. At present, this is a manual process. In the case they do not have an organization identifier, this can help them create one by gathering the information needed. (aka tag some information)

- Project name, 

  - Brief name
  - Organization identifier (optional)
  - Logo (optional)

- Contacts

  - PI/Leader
  - Datamanager/Technical
  - Others

- Description

  - What do you do

  - Keywords

  - Data

    - How many files
    - How many megabytes
    - what are the data types/formats
    - How frequently are is data updated/refreshed/added
    - API’s or methods (api, s3, ftp, http, etc).

  - How does your community use and access your data, presently? Do the download to laptop, use from cloud, use in Community Infrastructure

  - Links to how people are using your data (undergrad lab tutorials, notebooks, papers, etc)

- Web Presence

  - Website
  - Sitemap
  - API’s, and api documentation.




#### * * *


#### What do we need to help assess you data

We need to assess your data, so we can understand the complexity of data used in your community. This may not need to be done by first working session, but if you can this would help direct our team.

- Data

  - Example datasets

    - Format
    - Type
    - Est size
    - Links to an example or two
    - How do community members/applications access this data


- Tools

  - Example tools

    - Name
    - Execution env
    - documentation/tutorial/paper

- Search terms

  - If you were looking for your data, how might you search for it?


#### What do we need to help assess you Schema.org Dataset Metadata


#### .

- We want to evaluate your implementation of  Science on schema
- We want to review your implementation of an XML  sitemap, or a ‘sitegraph’
- We need to have some high bandwidth conversations when we ask for revisions on the Schema or Sitemap
- We need Input on search terms that can be used to access you data

We will help you do this in a work session(s) to help your team  learn the tools, and use best practices.

Science on schema guidance… is [here](https://github.com/ESIPFed/science-on-schema.org).

If you do not yet have schema.org Dataset data on your site, here is the Science On Schema Getting Started guidance. Even if you do have science on schema, please review the latest guidance.

Now, if you have  schema.org Dataset data on your site, please test a few pages in the validator.schema.org and provide the links in the onboarding form.

If you have not developed schema.org Dataset metadata, it can look complex, but it can be minimal, initially. But we would hope that Science On Schema can be used to more fully describe your data.

**How the data and website evaluation process works.********(INSERT DECISION TREE **[**HERE**](https://github.com/earthcube/ec/blob/master/doc/repo_onboarding.md)**)**

There are tools assess your data:

- If you have JSONLD on your pages: Link to validator.schema.org

- Detailed Evaluation using SHACL

  - Do we have a way to do a single SHACL?

- Sitemap checker

Steps for Evaluating:

- From your site, go to a dataset HTML page

- Test a page in validator.schema.org,

  - (insert) Links to several types of data

- Grab XML sitemap

  - Test a loc attribute  in validator.schema.org,

- Run sitemap checker

- (future) Evaluate in SHACL

- Communicate with team that you think you are ready. 

  - Provide links to sitemap and validator.schema.org

- We will attempt to load and build a tenant.

- When tenant is built, 

  - We provide links to datasets, tools in the tennant ui
  - Test with keywords.
  - Approve that information is present
  - …. 




#### * * *





### Workflow:

Do you have Science on Schema implemented? 

Yes go to step N

No go to Step 1

You have Science on Schema

- Sitemap
- Example validator.schema.org links with your 
- Testing with shacl shapes.




## 


### Section 3: What decoder/Geodes will do

What decoder tests that need to be done

Quality checks that we do to prepare for onboarding

- Sitemap, and urls
- Jsonld extraction,
- Initial qa and loading into a tenant for you to test your data
- Shacl Evaluation

Once things are running, what we plan to provide:

- Loading to production instance

  -

- Monthly Reports (under Development)

- Yearly Reports  (under Development)

