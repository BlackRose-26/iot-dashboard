#pragma once
#include <Arduino.h>
struct RequestJob {
  String kind;
  String path;
  String body;
  String boot;
  int status=0;
  String response;
};
