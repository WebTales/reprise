from pymongo import MongoClient
import params
import urllib2
import json
import time
import mimetypes
import os
import gridfs

client = MongoClient(params.connexionString)
db = client[params.dbName]
fs = gridfs.GridFS(db)

url = 'https://api.discogs.com/database/search?type=master&per_page=100'

auth = {'Discogs token=SDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOnSDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOn'}
headers = {'Authorization': 'Discogs token=SDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOn'}
data = None
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
releases = json.loads(response.read())

def insertRelease(id, url):

    # Check for existing release
    found = db.Contents.find_one({'typeId' : params.releaseTypeId, 'discogsid' : id},{'_id':1})
    if (found is None):
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        release = json.loads(response.read())
        titre = release['title']
        titre = titre.encode('UTF-8')
        resume = titre
        createTime = int(time.time())
        lastUpdateTime = createTime
        taxonomies = {}
        fields = {}

        # id
        fields['discogsid'] = release['id']

        # insert images
        images = []
        if ('images' in release):
            for image in release['images']:
                visuel_id = str(insertDAM(image['uri'],titre))
                images.append(visuel_id)
        fields['images'] = images

        # insert videos
        videos = []
        if ('videos' in release):
            for video in release['videos']:
                videos.append({'url': video['uri']})
        fields['videos'] = videos

        # insert fields and taxonomies
        for key in release:
            if (key in params.vocabularies):
                taxonomies[params.vocabularies[key]] = insertTaxo(params.vocabularies[key], release[key])
            if (key in params.fields):
                fields[params.fields[key]] = release[key]

        # insert artists
        artists = []
        if ('artists' in release):
            for artist in release['artists']:
                artist_id = str(insertArtist(artist['id'], artist['resource_url']))
                if artist_id is not None:
                    artists.append(artist_id)
        fields['artists'] = artists

        writeWorkspace = "global"
        target = ["global"]

        object = {
            "text" : titre,
            "typeId" : params.releaseTypeId,
            "version" : 1,
            "online" : True,
            "lastUpdateTime" : lastUpdateTime,
            "createTime" : createTime,
            "isProduct" : False,
            "productProperties" : "",
            "workspace" : {
                "fields" : fields,
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : taxonomies,
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "en" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : ""
                        },
                        "locale" : "en"
                    }
                },
                "nativeLanguage" : "en"
            },
            "live" : {
                "fields" : fields,
                "status" : "published",
                "startPublicationDate" : "",
                "endPublicationDate" : "",
                "taxonomy" : taxonomies,
                "target" : target,
                "writeWorkspace" : writeWorkspace,
                "pageId" : "",
                "maskId" : "",
                "blockId" : "",
                "i18n" : {
                    "en" : {
                        "fields" : {
                            "text" : titre,
                            "urlSegment" : "",
                            "summary" : "",
                        },
                        "locale" : "en"
                    }
                },
                "nativeLanguage" : "en"
            },
            "lastUpdateUser" : {
                "id" : params.createUserId,
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : params.createUserId,
                "login" : "admin",
                "fullName" : "admin"
            }
        }

        content_id = db.Contents.insert_one(object).inserted_id
        print('New release: ' + id)
    else:
        print('Skiping release '+ found +': already exists')

def insertArtist(id, url):
    print(url)
    if (url==='https://api.discogs.com/artists/194'):
        return None
    # Check for existing artist
    found = db.Contents.find_one({'typeId' : params.artistTypeId, 'discogsid' : id},{'_id':1})
    if (found is None):
        request = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(request)
            artist = json.loads(response.read())
            titre = artist['name']
            titre = titre.encode('UTF-8')
            resume = titre
            createTime = int(time.time())
            lastUpdateTime = createTime
            taxonomies = {}
            fields = {}
            # id
            fields['discogsid'] =  artist['id']
            # insert images
            images = []
            if ('images' in artist):
                for image in artist['images']:
                    visuel_id = str(insertDAM(image['uri'],titre))
                    images.append(visuel_id)
            fields['images'] = images
            # insert urls
            urls = []
            if ('urls' in artist):
                for url in artist['urls']:
                    urls.append({'url': url})
            fields['urls'] = urls
            # insert fields and taxonomies
            for key in artist:
                if (key in params.vocabularies):
                    taxonomies[params.vocabularies[key]] = insertTaxo(params.vocabularies[key], artist[key])
                if (key in params.fields):
                    fields[params.fields[key]] = artist[key]
            writeWorkspace = "global"
            target = ["global"]
            object = {
                "text" : titre,
                "typeId" : params.artistTypeId,
                "version" : 1,
                "online" : True,
                "lastUpdateTime" : lastUpdateTime,
                "createTime" : createTime,
                "isProduct" : False,
                "productProperties" : "",
                "workspace" : {
                    "fields" : fields,
                    "status" : "published",
                    "startPublicationDate" : "",
                    "endPublicationDate" : "",
                    "taxonomy" : taxonomies,
                    "target" : target,
                    "writeWorkspace" : writeWorkspace,
                    "pageId" : "",
                    "maskId" : "",
                    "blockId" : "",
                    "i18n" : {
                        "en" : {
                            "fields" : {
                                "text" : titre,
                                "urlSegment" : "",
                                "summary" : ""
                            },
                            "locale" : "en"
                        }
                    },
                    "nativeLanguage" : "en"
                },
                "live" : {
                    "fields" : fields,
                    "status" : "published",
                    "startPublicationDate" : "",
                    "endPublicationDate" : "",
                    "taxonomy" : taxonomies,
                    "target" : target,
                    "writeWorkspace" : writeWorkspace,
                    "pageId" : "",
                    "maskId" : "",
                    "blockId" : "",
                    "i18n" : {
                        "en" : {
                            "fields" : {
                                "text" : titre,
                                "urlSegment" : "",
                                "summary" : "",
                            },
                            "locale" : "en"
                        }
                    },
                    "nativeLanguage" : "en"
                },
                "lastUpdateUser" : {
                    "id" : params.createUserId,
                    "login" : "admin",
                    "fullName" : "admin"
                },
                "createUser" : {
                    "id" : params.createUserId,
                    "login" : "admin",
                    "fullName" : "admin"
                }
            }

            artist_id = db.Contents.insert_one(object).inserted_id
            print('New artist: ' + id)
            return artist_id
        except urllib2.HTTPError, e:
            print e.code
            print e.msg
        return None
    else:
        print('Skiping artist '+ found +': already exists')

def insertTaxo(vocabulary,terms):
    results = []
    for term in terms:
        termObject = db.TaxonomyTerms.find_one({'vocabularyId':vocabulary,'text':term},{'_id':1})
        if (termObject is None):
            term = {
                "text" : term,
                "vocabularyId" : vocabulary,
                "parentId" : "root",
                "leaf" : True,
                "expandable" : False,
                "nativeLanguage" : "en",
                "i18n" : {
                    "en" : {
                        "text" : term,
                        "locale" : "en"
                    }
                }
            }
            term_id = str(db.TaxonomyTerms.insert_one(term).inserted_id)
        else:
            term_id = str(termObject['_id'])
        results.append(term_id)
    return results

def insertDAM(visuel,titre):

    fileName = os.path.basename(visuel)
    damObject = db.Dam.find_one({'originalFileId':fileName},{'_id':1})
    if (damObject is None):
        filePath = params.baseUrl + visuel
        contentType, fileEncoding =  mimetypes.guess_type(filePath)
        image = urllib2.urlopen(filePath)
        meta = image.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        meta = {
            'Content-Type': contentType
        }
        originalFileId = fs.put(image, filename=fileName, metadata=meta)
        createTime = int(time.time())
        lastUpdateTime = createTime
        dam = {
            "typeId" : params.damTypeId,
            "directory" : "notFiled",
            "mainFileType" : "Image",
            "title" : titre,
            "taxonomy" : [ ],
            "writeWorkspace" : "global",
            "target" : ["global"],
            "originalFileId" : fileName,
            "Content-Type" : contentType,
            "nativeLanguage" : "en",
            "i18n" : {
                "en" : {
                    "fields" : {
                        "title" : titre
                    },
                    "locale" : "en"
                }
            },
            "fileSize" : fileSize,
            "version" : 1,
            "lastUpdateUser" : {
                "id" : params.createUserId,
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : params.createUserId,
                "login" : "admin",
                "fullName" : "admin"
            },
            "createTime" : createTime,
            "lastUpdateTime" : lastUpdateTime
        }
        dam_id = db.Dam.insert_one(dam).inserted_id
    else:
        dam_id = damObject['_id']
    return dam_id

for item in releases['results']:
    insertRelease(item['id'], item['resource_url'])
