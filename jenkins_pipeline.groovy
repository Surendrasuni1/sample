








pipeline{
	agent{label 'slave'}
		stages{
			stage('Clean workspace'){
				steps{
				  cleanWs()
				  }
			}	  
			stage('clone the source code'){
				steps{
					echo 'In SCM Stage'
					
					git credentialsId: '00bc114b-de10-4150-b985-7aac6d715798', url: 'https://github.com/Surendrasuni1/sample', branch:'master'
				}	
		
			}
			stage('shell script'){
			    steps{
				   sh '''
				   
						pwd
						ls
						mkdir jen
						ls
				   
				   '''
				
				}
			}
			stage('last stage of the code'){
				steps{
				
				echo 'All The Best!!!!!'
				
				}
			
			
			
			}
		
		}




	}
