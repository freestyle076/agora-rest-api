//
//  main.swift
//  UploadImage
//
//  Created by Kyle Handy on 11/17/14.
//  Copyright (c) 2014 Kyle Handy. All rights reserved.
//

import Foundation
import AppKit


//create url request pointed to api method url
var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.121:8000/uploadimage/")!)
request.HTTPMethod = "POST"
//var request = NSMutableURLRequest(URL: NSURL(string: "http://147.222.165.133:8000/uploadimage/")!)
var session = NSURLSession.sharedSession()

//create image object and convert to JSON passable UTF-8 encoded string
//image urls
var imageUrls:[NSURL] = [NSURL(fileURLWithPath: "/Users/kylehandy/Desktop/thisguy.png")!,NSURL(fileURLWithPath: "/Users/kylehandy/Desktop/thisotherguy.png")!]
var imageData:NSData = NSData(contentsOfURL: NSURL(fileURLWithPath: url)!)!
let base64String = imageData.base64EncodedStringWithOptions(NSDataBase64EncodingOptions(0))
println(base64String)
//var imageString:NSString = NSString(data: imageData, encoding: NSUTF8StringEncoding)!
//var imageString:String = NSData.hexadecimalString(imageData)()


var caption = "This picture is so cray-cray it makes me say-say i'm going HAAM today-day" //set caption value here
var position =  1 //set position value here

var params = ["position":position, "image":base64String] as Dictionary<String, AnyObject>

var err: NSError?
request.HTTPBody = NSJSONSerialization.dataWithJSONObject(params, options: nil, error: &err)
request.addValue("application/json", forHTTPHeaderField: "Content-Type")
request.addValue("application/json", forHTTPHeaderField: "Accept")

var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
    println(response)
    
})

task.resume()



sleep(10)


