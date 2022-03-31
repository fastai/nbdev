#!/usr/bin/env bash

nbprocess_docs --path nbs --dest docusaurus/docs
cd docusaurus/                                  
npm run build                                   
cd ..                                           
rm -rf docs
mv docusaurus/build docs                        
cp docs_src/CNAME docs/                         

