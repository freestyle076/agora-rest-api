//
//  main.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation


var api_requester: AgoraRequester = AgoraRequester()

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

/*
api_requester.ViewPost("Household", id: 284,
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
*/


//----------------------------------------userposts----------------------------------------



let username = "jquiring"
let divider_date_time = ""
//let divider_date_time = "02/24/2015 01:03:14"
let older = "1"

let params = ["username":username,
    "divider_date_time":divider_date_time,
    "older":older]
    as Dictionary<String,AnyObject>


api_requester.POST("userposts/",params:params,
    success: {parseJSON -> Void in
        let posts: AnyObject = parseJSON["posts"]!
        let more = parseJSON["more_exist"] as String
        let recent_del: String = parseJSON["recent_post_deletion"] as String

        if posts.count > 0{
            for i in 0...(posts.count - 1){
                let post: AnyObject! = posts[i]
                let postID = post["id"]! as Int
                let title = post["title"]! as String
                let post_date_time = post["post_date_time"]! as String
                let display_value = post["display_value"]! as String
                
                print(title + " ")
                println(postID)
                
                //THE THUMBNAIL IMAGE IS PROCESSED HERE
                let imageString = post["image"]! as String
                if !imageString.isEmpty {
                    let imageData = NSData(base64EncodedString: imageString, options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                    
                    //do stuff with the image here
                }
                else{
                    //CASE IN WHICH THE POST HAD NO IMAGE
                }

            }
        }
    },
    failure: {code,message -> Void in
        if(code == 500){
            println("500 user")
            //server error
        }
        else if (code == 599){
            println("599 user")
            //timeout
        }
        else if (code == 58){
            println("58 user")
            //no internet connection
        }
    }
)



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


//----------------------------------------filterposts----------------------------------------

/*
//set filter parameters
let categories:[String] = ["Household"] //empty list means all categories
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



api_requester.POST("postquery/", params: params,
    success: {parseJSON -> Void in
                
        var message = parseJSON["message"] as String
        println(message)
        let posts: AnyObject = parseJSON["posts"]!
        println(posts.count)
        if posts.count > 0{
            for i in 0...(posts.count - 1){
                let post: AnyObject! = posts[i] //just so we don't keep re-resolving this reference
                
                //get the easy ones, title and display_value
                //HERE ARE THE TEXTUAL INFORMATION PIECES FOR THE POST
                let title = post["title"] as String
                let display_value = post["display_value"]! as String
                let postID = post["id"]! as Int
                let category = post["category"]! as String
                let post_date_time = post["post_date_time"]! as String
                println(display_value + " " + title + " - " + category)
                
                //THE THUMBNAIL IMAGE IS PROCESSED HERE
                let imageString = post["image"]! as String
                if !imageString.isEmpty {
                    let imageData = NSData(base64EncodedString: imageString, options: NSDataBase64DecodingOptions.IgnoreUnknownCharacters)!
                    
                    //do stuff with the image here
                }
                else{
                    //CASE IN WHICH THE POST HAD NO IMAGE
                }
            }
        }
    
    },
    failure: {code,message -> Void in
        if code == 500 {
            //500: Server failure
            println("Server Failure!!!!!")
        }
        else if code == 400 {
            //400: Bad Client Request
            println("Bad Request!!!!!")
        }
        else if code == 58 {
            //58: No Internet Connection
            println("No Connection!!!!!")
        }
        else if code == 599 {
            //599: Request Timeout
            println("Timeout!!!!!")
        }
    }
)
*/


sleep(21)
println("done sleeping")