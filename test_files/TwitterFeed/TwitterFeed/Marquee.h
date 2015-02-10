//
//  Marquee.h
//  TwitterFeed
//
//  Created by Trenton Miller on 2/9/15.
//  Copyright (c) 2015 Trenton Miller. All rights reserved.
//

#ifndef TwitterFeed_Marquee_h
#define TwitterFeed_Marquee_h
#import Foundation

enum MarqeeDirection{
    DirectionUnset,
    DirectionLeftToRight,
    DIrectionRightToLeft
};

var direction: MarqeeDirection

var tileDuration: NSTimeInterval

var TileImage: UIImage

#endif
