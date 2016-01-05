from pymongo import MongoClient
import urllib2
import base64
import gridfs
import mimetypes
import time
import os
import lxml
import params

client = MongoClient(params.connexionString)
db = client[params.dbName]
fs = gridfs.GridFS(db)

def insertContent(title, subtitle, price, description, photo, ville, codepostal, typebien, surface, lat, lon):
      
    # default values
    createTime = int(time.time())
    lastUpdateTime = createTime
    
    # insert visuel
    if photo is not None:
        visuel_id = str(insertDAM(photo,title,"Image"))
    else:
        visuel_id = None
   
    writeWorkspace = "global"
    target = ["global"]
     
    object = {
        "text" : title,
        "typeId" : params.typeId,
        "version" : 1,
        "online" : True,
        "lastUpdateTime" : lastUpdateTime,
        "createTime" : createTime,
        "isProduct" : False,
        "productProperties" : "",
        "workspace" : {
            "fields" : {
                "image" : visuel_id,
                "position" : {
                    "address" : "",
                    "location : {
                        "type : "Point", 
                        "coordinates : [lon, lat]
                    },
                    "lat": lat,
                    "lon": lon
                }
            },
            "status" : "published",
            "startPublicationDate" : "",
            "endPublicationDate" : "",
            "target" : target,
            "writeWorkspace" : writeWorkspace,
            "pageId" : "",
            "maskId" : "",
            "blockId" : "",
            "i18n" : {
                "fr" : {
                    "fields" : {
                        "text" : title,
                        "urlSegment" : "",
                        "summary" : subtitle,
                        "price" : price,
                        "description" : description, 
                        "ville" : ville,
                        "codepostal" : codepostal,
                        "typebien" : typebien,
                        "surface" : surface
                    },
                    "locale" : "fr"
                }
            },
            "nativeLanguage" : "fr"
        },
        "live" : {
            "fields" : {
                "image" : visuel_id,
                "position" : {
                    "address" : "",
                    "location : {
                        "type : "Point", 
                        "coordinates : [lon, lat]
                    },
                    "lat": lat,
                    "lon": lon
                }
            },
            "status" : "published",
            "startPublicationDate" : "",
            "endPublicationDate" : "",              
            "target" : target,
            "writeWorkspace" : writeWorkspace,
            "pageId" : "",
            "maskId" : "",
            "blockId" : "",
            "i18n" : {
                "fr" : {
                    "fields" : {
                        "text" : title,
                        "urlSegment" : "",
                        "summary" : subtitle,
                        "price" : price,
                        "description" : description, 
                        "ville" : ville,
                        "codepostal" : codepostal,
                        "typebien" : typebien,
                        "surface" : surface
                    },
                    "locale" : "fr"
                }
            },
            "nativeLanguage" : "fr"
        },
        "lastUpdateUser" : {
            "id" : "5659ba5e1a6c7ed7238b456e",
            "login" : "admin",
            "fullName" : "admin"
        },
        "createUser" : {
            "id" : "5659ba5e1a6c7ed7238b456e",
            "login" : "admin",
            "fullName" : "admin"
        }
    }
    
    content_id = db.Contents.insert_one(object).inserted_id
    #print(object)

def insertDAM(visuel,titre,main_filetype):

    if main_filetype == "Image":
        typeId = params.typeImage
    if main_filetype == "Document":
        typeId = params.typeDocument   
    
    fileName = os.path.basename(visuel)
    damObject = db.Dam.find_one({'title':fileName},{'_id':1})
    if (damObject is None):
        filePath = params.baseUrl + visuel
        contentType, fileEncoding =  mimetypes.guess_type(filePath)
        image = urllib2.urlopen(filePath)
        meta = image.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        ct = {
            'Content-Type': contentType
        }
        originalFileId = fs.put(image, content_type=contentType, filename=fileName, mainFileType=main_filetype, text=titre, **ct)
        createTime = int(time.time())
        lastUpdateTime = createTime
        dam = {
            "typeId" : typeId,
            "directory" : "notFiled",
            "mainFileType" : main_filetype,
            "title" : fileName,
            "taxonomy" : [ ],
            "writeWorkspace" : "global",
            "target" : ["global"],
            "originalFileId" : str(originalFileId),
            "Content-Type" : contentType,
            "nativeLanguage" : "fr",
            "i18n" : {
                "fr" : {
                    "fields" : {
                        "title" : fileName,
                        "alt" : titre
                    },
                    "locale" : "fr"
                }
            },
            "fileSize" : fileSize,
            "version" : 1,
            "lastUpdateUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
                "login" : "admin",
                "fullName" : "admin"
            },
            "createUser" : {
                "id" : "5659ba5e1a6c7ed7238b456e",
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