//
//  main.swift
//  AgoraRequesterTester
//
//  Created by Kyle Handy on 2/10/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

println("Run dem jewels")

var api_requester: AgoraRequester = AgoraRequester()

//set filter parameters
let categories:[String] = ["Books"] //empty list means all categories
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
                println(post_date_time + " " + title + " - " + category)
                
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
            //server failure
        }
        else if code == 400 {
            //bad request by client
        }
        else if code == 58 {
            //no connection
        }
        else if code == 599 {
            //timeout
        }
})