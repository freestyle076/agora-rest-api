//
//  main.swift
//  FilterPosts
//
//  Created by Kyle Handy on 1/11/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//kyle
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/postquery/")!)
//trenton
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/postquery/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()


//set filter parameters
let categories:[String] = [] //empty list means all categories
let keywordSearch:String = "" //empty string means no keyword search
let min_price = "5" //"" means no min_price
let max_price = "100" //"" means no max_price
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

//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")

var response_has_returned = false

//define NSURLSession data task with completionHandler call back function
var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    
    
    if error != nil{
        println("Error!")
    }
    
    //downcast NSURLResponse object to NSHTTPURLResponse
    if let httpResponse = response as? NSHTTPURLResponse {
        
        //get the status code
        var status_code = httpResponse.statusCode
        
        //200 = OK: carry on!
        if(status_code == 200){
            
            var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
            if(err != nil) {
                println(err!.localizedDescription)
                let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
                println("Error could not parse JSON: '\(jsonStr)'")
            }
                
            else {
                
                //response code is OK, continue with parsing JSON and reading response data
                //THIS IS WHERE RESPONSE HANDLING CODE SHOULD GO

                
                let posts: AnyObject = parseJSON!["posts"]!
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
                        print(title + " - " + category + " - ")
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
            }
        }
            
        //400 = BAD_REQUEST: error in creating user, display error!
        else if(status_code == 400){
            var parseJSON = NSJSONSerialization.JSONObjectWithData(data, options: NSJSONReadingOptions(0), error: &err) as? Dictionary<String,AnyObject>
            if(err != nil) {
                println(err!.localizedDescription)
                let jsonStr = NSString(data: data, encoding: NSUTF8StringEncoding)
                println("Error could not parse JSON: '\(jsonStr)'")
            }
            else{
            }
        }
            
        //500 = INTERNAL_SERVER_ERROR. Oh snap *_*
        else if(status_code == 500){
            println("The server is down! I blame Schnagl")
        }
        
        
    }
    else {
        println("Error in casting response, data incomplete")
    }

    
    response_has_returned = true
    
})

task.resume()


var count = 0
while count < 8 && !response_has_returned{
    count++
    sleep(1)
}


if !response_has_returned {
    session.invalidateAndCancel()
    //handle no response
}



