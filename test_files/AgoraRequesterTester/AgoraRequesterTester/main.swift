//
//  main.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation


var api_requester: AgoraRequester = AgoraRequester()

//----------------------------------------userposts----------------------------------------

/*
let username = "jquiring"
let divider_date_time = ""
//let divider_date_time = "02/24/2015 01:03:14"
let older = "1"

let params = ["username":username,
    "divider_date_time":divider_date_time,
    "older":older]
    as Dictionary<String,AnyObject>


api_requester.UserPosts(params,
    info: {parseJSON -> Void in
        println("info received")
    },
    imageReceived: {category,postID,imageData -> Void in
        //imageReceived function only called IF there is an image
        //no point in running this function just to determine there is no image...
        println("received image for " + category + " " + String(postID))
    },
    failure: {code,message -> Void in
        println("Failure!!!")
        println(code)
        println(message)
    }
)*/


//----------------------------------------postquery----------------------------------------

/*
//set filter parameters
let categories:[String] = ["Household","Events"] //empty list means all categories
let keywordSearch:String = "" //empty string means no keyword search
let min_price = "" //"" means no min_price
let max_price = "" //"" means no max_price
let free = "0" //false means not free only, true means is free only
let divider_date_time = ""
//let divider_date_time = "01/28/2015 10:26:54"
let older = "1"

let params = ["categories":categories,
    "keywordSearch":keywordSearch,
    "min_price":min_price,
    "max_price":max_price,
    "free":free,
    "divider_date_time":divider_date_time,
    "older":older]
    as Dictionary<String,AnyObject>

api_requester.PostQuery(params,
    info: {parseJSON -> Void in
        println("info received")
    },
    imageReceived: {category,postID,imageData -> Void in
        //imageReceived function only called IF there is an image
        //no point in running this function just to determine there is no image...
        print("Received image for" + category + " ")
        println(postID)
        imageData.writeToFile("/Users/kylehandy/Desktop/" + category + String(postID) + ".png",atomically: false)
    },
    failure: {code,message -> Void in
        print("failure!!")
        print(code)
        println(" " + message)
    }
)
*/

//----------------------------------------viewposts----------------------------------------

for x in 1...100{
    api_requester.ViewPost("Electronics", id: 325,
        info: {parseJSON -> Void in
            println("info received")
        },
        image1: {imageData -> Void in
            if imageData == nil{
                println("image received 1")
                //case where image1 is nil
            }
            else{
                println("image received 1")
                //case where image1 exists
            }
        },
        image2: {imageData -> Void in
            if imageData == nil{
                //case where image2 is nil
            }
            else{
                //case where image2 exists
            }
            
        },
        image3: {imageData -> Void in
            if imageData == nil{
                //case where image3 is nil
            }
            else{
                //case where image3 exists
            }
        },
        failure: {code,message -> Void in
            println("failure")
            println(code)
            println(message)
        }
    )
}



//----------------------------------------ldapauth----------------------------------------

/*
api_requester.LdapAuth("khandy", password: "Rusty3220",
    success: { parseJSON -> Void in
        println("success")
        println(parseJSON)
    },
    failure: {code,message -> Void in
        if(code == 500){
            //server error
            println(500)
        }
        else if (code == 599){
            //timeout
            println(599)
        }
        else if (code == 58){
            //no internet connection
            println(58)
        }
    },
    badCreds: { () -> Void in
        println("bad")
        //function for bad credentials
    }
)*/



sleep(5000)
println("done sleeping")