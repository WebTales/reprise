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

url = 'https://api.discogs.com/database/search?type=release&per_page=10'

auth = {'Discogs token=SDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOnSDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOn'}
headers = {'Authorization': 'Discogs token=SDRLVIGRXKJYqpWuvCGMDnUtIaYchavROyvisOOn'}
data = None
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
releases = json.loads(response.read())

def insertContent(release):
 # content_id, titre, resume, texte, visuel, objectType, taxo, workspace

    # get proper encoding
    titre = release['title']
    titre = titre.encode('UTF-8')
    resume = titre

    # default values
    createTime = int(time.time())
    lastUpdateTime = createTime

    # insert visuel
    if release['thumb']:
        visuel_id = str(insertDAM(release['thumb'],titre))
    else:
        visuel_id = None

    #if taxo == "" or taxo is None:
    taxo_id = None
    #else:
    #    taxo_id = [taxo]

    writeWorkspace = "global"
    target = ["global"]

    object = {
        "text" : titre,
        "typeId" : params.contentTypeId,
        "version" : 1,
        "online" : True,
        "lastUpdateTime" : lastUpdateTime,
        "createTime" : createTime,
        "isProduct" : False,
        "productProperties" : "",
        "workspace" : {
            "fields" : {
                "thumbnail" : visuel_id
            },
            "status" : "published",
            "startPublicationDate" : "",
            "endPublicationDate" : "",
            "taxonomy" : {
                "navigation" : taxo_id
            },
            "target" : target,
            "writeWorkspace" : writeWorkspace,
            "pageId" : "",
            "maskId" : "",
            "blockId" : "",
            "i18n" : {
                "fr" : {
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
            "fields" : {
                "thumbnail" : visuel_id
            },
            "status" : "published",
            "startPublicationDate" : "",
            "endPublicationDate" : "",
            "taxonomy" : {
                "navigation" : taxo_id
            },
            "target" : target,
            "writeWorkspace" : writeWorkspace,
            "pageId" : "",
            "maskId" : "",
            "blockId" : "",
            "i18n" : {
                "fr" : {
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

    #content_id = db.Contents.insert_one(object).inserted_id
    print(object)

def insertDAM(visuel,titre):

    fileName = os.path.basename(visuel)
    damObject = db.Dam.find_one({'title':fileName},{'_id':1})
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

for release in releases['results']:
    insertContent(release)