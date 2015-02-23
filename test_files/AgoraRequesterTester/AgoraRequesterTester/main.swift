//
//  main.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation


var api_requester: AgoraRequester = AgoraRequester()

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

println("request fired")

api_requester.LdapAuth("khandy", password: "Rusty3220",
    success: { parseJSON -> Void in
        println(parseJSON)
    },
    failure: { code -> Void in
        println("error")
        println(code)
    },
    badCreds: { () -> Void in
        println("Invalid creds")
    }
)

/*
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
    failure: {code -> Void in
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