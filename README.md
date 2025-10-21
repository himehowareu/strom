import filename 
this command will import the file into the current file 

macro name arg1 arg2
{
  commands arg2
  commands arg1
}
the args will be replaced in the block 

block_macro name args block
{
  command arg 
  block
}
this macro will take the next block after it is called as an arg 

runtime
{
  python code 
}
the python code will be evaled
