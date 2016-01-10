#include<stdio.h>
#include<string.h>
#include<stdlib.h>

//Implements a version of bubble sort

int main(){
  int i,j,n;
  char str[200000][20];
  char temp[30];
  i=0;
  n=0;
  
  while(fgets(str[i],20,stdin)!=NULL)
  {
      i++;
      n++;
  }
  
  for(i=0;i<=n;i++)
      for(j=i+1;j<=n;j++){
           if(strcmp(str[i],str[j])>0){
              strcpy(temp,str[i]);
              strcpy(str[i],str[j]);
              strcpy(str[j],temp);
           }
      }
  
  for(i=0;i<=n;i++)
      puts(str[i]);
  return 0;
}
