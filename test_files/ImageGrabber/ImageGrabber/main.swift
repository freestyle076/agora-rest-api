//
//  main.swift
//  FilterPosts
//
//  Created by Kyle Handy on 1/11/15.
//  Copyright (c) 2015 Kyle Handy. All rights reserved.
//

import Foundation

//create a mutable request with api view path /createuser/, set method to POST
//server
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.3:8000/getimage/")!)
request.HTTPMethod = "POST"

//open NSURLSession
var session = NSURLSession.sharedSession()


let params = ["category":"Electronics","post_id":String(297),"picture_id":"0"]
    as Dictionary<String,AnyObject>

//Load body with JSON serialized parameters, set headers for JSON! (Star trek?)
var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
//request.addValue("image/png", forHTTPHeaderField: "Accept")

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
            
            let intermediateBoundaryString: NSString = "--$AGORA_boundary$"
            let intermediateBoundaryData: NSData = intermediateBoundaryString.dataUsingEncoding(NSUTF8StringEncoding)!
            let finalBoundaryString: NSString = "--$AGORA_boundary$--"
            let finalBoundaryData: NSData = finalBoundaryString.dataUsingEncoding(NSUTF8StringEncoding)!
            let bracketString: NSString = "{"
            let bracketData: NSData = bracketString.dataUsingEncoding(NSUTF8StringEncoding)!
            let bracket2String: NSString = "}"
            let bracket2Data: NSData = bracket2String.dataUsingEncoding(NSUTF8StringEncoding)!
            let imageContentString: NSString = "Content-Type: image/png"
            let imageContentData: NSData = imageContentString.dataUsingEncoding(NSUTF8StringEncoding)!
            
            //find json range by searching for { }
            let bracketRange: NSRange = data.rangeOfData(bracketData, options: nil, range: NSMakeRange(0, data.length))
            let bracket2Range: NSRange = data.rangeOfData(bracket2Data, options: nil, range: NSMakeRange(0, data.length))
            
            //extract json data from response body
            let jsonRange: NSRange = NSUnionRange(bracketRange, bracket2Range)
            let jsonData: NSData = data.subdataWithRange(jsonRange)
            var parseJSON = NSJSONSerialization.JSONObjectWithData(jsonData, options: NSJSONReadingOptions(0), error: &err) as Dictionary<String,AnyObject>
            
            let imageFlag = parseJSON["image"] as Bool
            var imageData: NSData?
            if imageFlag{
                let imageBoundaryRange: NSRange = data.rangeOfData(imageContentData, options: nil, range: NSMakeRange(jsonRange.location, data.length - jsonRange.location))
                println(imageBoundaryRange)
                
                let finalBoundaryRange: NSRange = data.rangeOfData(finalBoundaryData, options: nil, range: NSMakeRange(0, data.length))
                println(finalBoundaryRange)
                
                let imageLocation = imageBoundaryRange.location + imageBoundaryRange.length + 4 // +2 ?
                let imageLength = finalBoundaryRange.location - imageLocation - 0
                let imageRange: NSRange = NSMakeRange(imageLocation, imageLength)
                
                imageData = data.subdataWithRange(imageRange)
                imageData!.writeToFile("/Users/kylehandy/Desktop/thisbestguyever.png", atomically: false)
            }
            else{
                imageData = nil
                println("No image")
            }
            println(parseJSON)
            
            
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
    
    
    
})

task.resume()


sleep(10)



