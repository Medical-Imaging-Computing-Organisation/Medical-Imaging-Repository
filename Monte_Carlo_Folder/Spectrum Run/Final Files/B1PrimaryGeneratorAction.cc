//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// $Id: B1PrimaryGeneratorAction.cc 94307 2015-11-11 13:42:46Z gcosmo $
//
/// \file B1PrimaryGeneratorAction.cc
/// \brief Implementation of the B1PrimaryGeneratorAction class

#include "B1PrimaryGeneratorAction.hh"

#include "G4LogicalVolumeStore.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4RunManager.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include "Randomize.hh" 
#include <cmath> 

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::B1PrimaryGeneratorAction()
: G4VUserPrimaryGeneratorAction(),
  fParticleGun(0), 
  fEnvelopeBox(0)
{
  G4int n_particle = 1;
  fParticleGun  = new G4ParticleGun(n_particle);
  // default particle kinematic
  G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
  G4String particleName;
  G4ParticleDefinition* particle
    = particleTable->FindParticle(particleName="gamma");
  fParticleGun->SetParticleDefinition(particle);
  fParticleGun->SetParticleEnergy(0.*keV);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::~B1PrimaryGeneratorAction()
{
  delete fParticleGun;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  //this function is called at the begining of ecah event
  //

  // In order to avoid dependence of PrimaryGeneratorAction
  // on DetectorConstruction class we get Envelope volume
  // from G4LogicalVolumeStore.
  
  G4double XY = 1*cm;
  G4double Z = 0;

  G4double size = 1.0; 
  G4double x0 = size * XY * (G4UniformRand()-0.5);
  G4double y0 = size * XY * (G4UniformRand()-0.5);
  G4double z0 = -0.5 * Z;
  
  fParticleGun->SetParticlePosition(G4ThreeVector(x0,y0,z0));

  //setting a vector representing the detector position
  G4ThreeVector d1position = G4ThreeVector(0, 0, 3.81*cm); 
  G4ThreeVector d2position = G4ThreeVector(-15, -15, 15);   
      
  //Setting detector sizes
  G4double d1size = 3.81*cm; 
  G4double d2size = 2.0; 
    
  //Calculating detector distances, polar and azimuthial angles
  G4double d1_r = d1position.mag(); 
  G4double d1_theta = d1position.theta(); 
  G4double d1_phi = d1position.phi(); 
  
  G4double d2_r = d2position.mag(); 
  G4double d2_theta = d2position.theta(); 
  G4double d2_phi = d2position.phi(); 

  //Using tan approximation to calculate an approximate angular deviation
  G4double d1_theta_max = d1size/d1_r;  
  G4double d1_phi_max = d1_theta_max;  
  
  G4double d2_theta_max = d2size/d2_r;  
  G4double d2_phi_max = d2_theta_max; 
  
  std::cout << "" << std::endl;
//   std::cout << "Angular deviation in polar and azimuthial for detector 1: " << d1_theta_max << " & " << d1_phi_max << std::endl;
//   std::cout << "Angular deviation in polar and azimuthial for detector 2: " << d2_theta_max << " & " << d2_phi_max << std::endl; 
  
  //Randomly generating a polar and azimuthial angle within the deviation
  G4double r1 = G4UniformRand(); 
  G4double polarAngle = 0;
  G4double azimuthialAngle =0; 
  
  //Using solid angle to scale the photon intensities
  G4double prob1 = (d1size)/(sqrt(2)*d1_r); 
  //G4double prob2 = (d2size)/(sqrt(2)*d2_r); 
  G4double prob2 = 0;
  
  G4double norm =  1/(prob1 + prob2); 
  
  //Once scaled these probabilities should account for solid angle and produce relaistic psuedo-Isotropic behaviour
  prob1 *= norm; 
  prob2 *= norm; 
  //std::cout << "The scaled relative probabilities due to geometry for detector 1 and 2 are: " << prob1 << ", " << prob2 << std::endl;
  
  if(r1 < prob1)
  {
    polarAngle = d1_theta + 2*(G4UniformRand()-0.5)*d1_theta_max; 
    azimuthialAngle = d1_phi + 2*(G4UniformRand()-0.5)*d1_phi_max;
  } 
  /*
  else
  {
    polarAngle = d2_theta + 2*(G4UniformRand()-0.5)*d2_theta_max; 
    azimuthialAngle = d2_phi + 2*(G4UniformRand()-0.5)*d2_phi_max;
  }
  */
  
//   std::cout << "Random particle momentum in polar: Theta & Phi: " << polarAngle << " & " << azimuthialAngle << std::endl;
  
  G4double px = std::sin(polarAngle)*std::cos(azimuthialAngle); 
  G4double py = std::sin(polarAngle)*std::sin(azimuthialAngle); 
  G4double pz = std::cos(polarAngle);
  
  G4ThreeVector direction(px, py, pz); 
  

  // Full Caesium 137 Source
  std::vector<G4double> intense = {1.99, 3.64, 0.348, 0.672, 0.213, 85.10};
  double tot_intense = 0;
  for (int i = 0; i<int(intense.size()); i ++){
      tot_intense += intense[i];
  } 
  

  fParticleGun->SetParticleMomentumDirection(direction); 
  G4double intense_rand = G4UniformRand() * tot_intense;
  
  if (intense_rand <= intense[0]){
      fParticleGun->SetParticleEnergy(31.827*keV);
  } 
  else if (intense_rand <= intense[0] + intense[1]){
      fParticleGun->SetParticleEnergy(32.194*keV);
  }
  else if (intense_rand <= intense[0] + intense[1] + intense[2]){
      fParticleGun->SetParticleEnergy(36.304*keV);
  }
  else if (intense_rand <= intense[0] + intense[1] + intense[2] + intense[3]){
      fParticleGun->SetParticleEnergy(36.378*keV);
  }
  else if (intense_rand <= intense[0] + intense[1] + intense[2] + intense[3] + intense[4]){
      fParticleGun->SetParticleEnergy(37.255*keV);
  } 
  else if (intense_rand <= intense[0] + intense[1] + intense[2] + intense[3] + intense[4] + intense[5]){
      fParticleGun->SetParticleEnergy(661.657*keV);
  }
  


/*
 std::cout << "" << std::endl;
 std::cout << "---------------------------" << std::endl;
 std::cout << "" << std::endl;
*/

  fParticleGun->GeneratePrimaryVertex(anEvent);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......