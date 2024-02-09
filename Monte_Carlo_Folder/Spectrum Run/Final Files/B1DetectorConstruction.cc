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
// $Id: B1DetectorConstruction.cc 94307 2015-11-11 13:42:46Z gcosmo $
//
/// \file B1DetectorConstruction.cc
/// \brief Implementation of the B1DetectorConstruction class

#include "B1DetectorConstruction.hh"

#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Cons.hh"
#include "G4Orb.hh"
#include "G4Sphere.hh"
#include "G4Trd.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Tubs.hh"
#include <G4VisAttributes.hh>

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::B1DetectorConstruction()
: G4VUserDetectorConstruction(),
  fScoringVolume(0)
{ 


}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::~B1DetectorConstruction()
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* B1DetectorConstruction::Construct()
{  
  // Get nist material manager
  G4NistManager* nist = G4NistManager::Instance();
  
  // Option to switch on/off checking of volumes overlaps
  //
  G4bool checkOverlaps = true;

  //     
  // World
  //
  G4double world_sizeXY = 3.5*m;
  G4double world_sizeZ  = 3.5*m;
  G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");
  
  G4Box* solidWorld = new G4Box("World",0.5*world_sizeXY, 0.5*world_sizeXY, 0.5*world_sizeZ);     //its size
      
  G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, world_mat, "World");            //its name
  
                                   
  G4VPhysicalVolume* physWorld = new G4PVPlacement(0,G4ThreeVector(),       //at (0,0,0)
                      logicWorld,            //its logical volume
                      "World",               //its name
                      0,                     //its mother  volume
                      false,                 //no boolean operation
                      0,                     //copy number
                      checkOverlaps);        //overlaps checking
                      
  
  // Walls
    G4double wall_thick = 20*cm;
    G4Material* wall_mat = nist->FindOrBuildMaterial("G4_CONCRETE");
    G4Box* wall_shape = new G4Box("wall",0.5*world_sizeXY, 0.5*world_sizeXY, 0.5*world_sizeZ);     //its size
    G4LogicalVolume* wall_log = new G4LogicalVolume(wall_shape, wall_mat, "World");            //its name
    G4VPhysicalVolume* wall = new G4PVPlacement(0,G4ThreeVector(),       //at (0,0,0)
                      wall_log,            //its logical volume
                      "wall",               //its name
                      logicWorld,                     //its mother  volume
                      false,                 //no boolean operation
                      0,                     //copy number
                      checkOverlaps);        //overlaps checking
  // Air
    G4double air_sizeXY = 0.5*world_sizeXY-wall_thick;
    G4double air_sizeZ = 0.5*world_sizeZ-wall_thick;
    G4Box* air_shape = new G4Box("air",air_sizeXY, air_sizeXY, air_sizeZ);     //its size
    G4LogicalVolume* air_log = new G4LogicalVolume(air_shape, world_mat, "air");            //its name
    G4VPhysicalVolume* air = new G4PVPlacement(0,G4ThreeVector(),       //at (0,0,0)
                      air_log,            //its logical volume
                      "air",               //its name
                      wall_log,                     //its mother  volume
                      false,                 //no boolean operation
                      0,                     //copy number
                      checkOverlaps);        //overlaps checking
  
  
    // Setting variables for detector construction
    
    // Colours
      G4VisAttributes* green = new G4VisAttributes(G4Colour::Green());
      green->SetVisibility(true);
      green->SetForceSolid(true);
      G4VisAttributes* red = new G4VisAttributes(G4Colour::Red());
      red->SetVisibility(true);
      red->SetForceSolid(true);
      G4VisAttributes* blue = new G4VisAttributes(G4Colour::Blue());
      blue->SetVisibility(true);
      blue->SetForceSolid(true);
      G4VisAttributes* yellow = new G4VisAttributes(G4Colour::Yellow());
      yellow->SetVisibility(true);
      yellow->SetForceSolid(true); 
    
     
    // Scintiallator
    G4double NaI_r = 3.81*cm;
	G4double NaI_hz = 3.81*cm;
	G4ThreeVector absorber_pos = G4ThreeVector(0,0,0);
	
	// MgO Reflector (2.7mm thick)
    	
    	// Face
    	G4double mface_r = NaI_r + 2.7*mm;
	    G4double mface_hz =  2.7*mm;
	    
	    // Back
    	G4double mback_hz =  2.7*mm;
    	G4double mback_r = mface_r;
    	
    	// Case
        G4double mCase_r = mface_r;
    	G4double mCase_hz = NaI_hz;
	
	// Face
	G4double face_r = mface_r + 3.2*mm;
	G4double face_hz =  0.5*mm;
	
	// Back
	G4double back_hz =  2*mm;
	G4double back_r = face_r;
	
	// Case
    G4double Case_r = face_r;
	G4double Case_hz = NaI_hz;
	G4double Case_p = Case_r*2;
    G4ThreeVector Case_pos = G4ThreeVector(0,0,Case_p*2);
    G4RotationMatrix* Case_rot = new G4RotationMatrix();
    Case_rot -> rotateX(0*deg);
	

	// create 2 in NaI crystal
	G4Tubs* NaI_shape = new G4Tubs("NaI", 0*mm, NaI_r, NaI_hz, 0*deg, 360*deg);
	G4LogicalVolume* NaI_log = new G4LogicalVolume(NaI_shape, nist->FindOrBuildMaterial("G4_SODIUM_IODIDE"), "NaI");

	
	// Create Aluminium Lightsheild around Detector
	
	// MgO Reflector 
	    // Face
    	G4Tubs* mface_shape = new G4Tubs("mface", 0*mm, mface_r, mface_hz, 0*deg, 360*deg);
    	G4LogicalVolume* mface_log = new G4LogicalVolume(mface_shape, nist->FindOrBuildMaterial("G4_Mg"), "mface");
    	
    	// Case
    	G4Tubs* mCase_shape = new G4Tubs("mCase", NaI_r, mCase_r, mCase_hz+mface_hz+mback_hz, 0*deg, 360*deg);
    	G4LogicalVolume* mCase_log = new G4LogicalVolume(mCase_shape, nist->FindOrBuildMaterial("G4_Mg"), "mCase");
    
    	
    	// Back
    	G4Tubs* mback_shape = new G4Tubs("mback", 0*mm, mback_r, mback_hz, 0*deg, 360*deg);
    	G4LogicalVolume* mback_log = new G4LogicalVolume(mback_shape, nist->FindOrBuildMaterial("G4_Mg"), "mback");
	
	// Face
	G4Tubs* face_shape = new G4Tubs("face", 0*mm, face_r, face_hz, 0*deg, 360*deg);
	G4LogicalVolume* face_log = new G4LogicalVolume(face_shape, nist->FindOrBuildMaterial("G4_Al"), "face");
	face_log->SetVisAttributes(red);
	
	// Case
	G4Tubs* Case_shape = new G4Tubs("Case", 0, Case_r, Case_hz+face_hz+back_hz+mface_hz+mback_hz, 0*deg, 360*deg);
	G4LogicalVolume* Case_log = new G4LogicalVolume(Case_shape, nist->FindOrBuildMaterial("G4_Al"), "Case");
	Case_log->SetVisAttributes(yellow);

	
	// Back
	G4Tubs* back_shape = new G4Tubs("back", 0*mm, back_r, back_hz, 0*deg, 360*deg);
	G4LogicalVolume* back_log = new G4LogicalVolume(back_shape, nist->FindOrBuildMaterial("G4_Al"), "back");
	back_log->SetVisAttributes(green);
	
	//Placement

    // Case
    G4VPhysicalVolume* Case = new G4PVPlacement(0, Case_pos, "Case", Case_log, air, false, 0, checkOverlaps);
    
    // MgO Reflector 
    
        // Case
        G4ThreeVector mCase_pos = G4ThreeVector();
        G4VPhysicalVolume* mCase = new G4PVPlacement(0, mCase_pos, "mCase", mCase_log, Case, false, 0, checkOverlaps);	
        
	    // Back
        G4ThreeVector mback_pos = G4ThreeVector(0,0, Case_hz+back_hz+face_hz);
        G4VPhysicalVolume* mback_physical = new G4PVPlacement(0, mback_pos, "mback", mback_log, Case, false, 0, checkOverlaps);	
        
        // Face
    	G4ThreeVector mface_pos = G4ThreeVector(0,0,-1*Case_hz-face_hz-back_hz);
        G4VPhysicalVolume* mface = new G4PVPlacement(0, mface_pos, "mface", mface_log, Case, false, 0, checkOverlaps);	
    
    // Back
    G4ThreeVector back_pos = G4ThreeVector(0,0, Case_hz+back_hz+face_hz+mback_hz+mface_hz);
    G4VPhysicalVolume* back_physical = new G4PVPlacement(0, back_pos, "back", back_log, Case, false, 0, checkOverlaps);	
    
    // Face
	G4ThreeVector face_pos = G4ThreeVector(0,0,-1*Case_hz-face_hz-back_hz-mback_hz-mface_hz);
    G4VPhysicalVolume* face = new G4PVPlacement(0, face_pos, "face", face_log, Case, false, 0, checkOverlaps);	
    
    // Scintillator
    G4VPhysicalVolume* NaI_absorber = new G4PVPlacement(0, absorber_pos, "absorber", NaI_log, Case, false, 0, checkOverlaps);
	NaI_log->SetVisAttributes(blue);


    // Table
    G4double table_sizeX = air_sizeXY;
    G4double table_sizeZ = air_sizeZ;
    G4double table_sizeY  = 7*cm;
    G4Material* table_mat = nist->FindOrBuildMaterial("G4_CELLULOSE_BUTYRATE");
    G4Box* table_shape = new G4Box("Table",table_sizeX, 0.5*table_sizeY, table_sizeZ);     //its size
    G4LogicalVolume* table_log = new G4LogicalVolume(table_shape, table_mat, "table");
    G4ThreeVector table_pos = G4ThreeVector(0,-table_sizeY/2 - Case_r, 0);
    G4VPhysicalVolume* table = new G4PVPlacement(0, table_pos, "Table", table_log, air, false, 0, checkOverlaps);
    
    /*
    // Lead 
    G4Material* block_mat = nist->FindOrBuildMaterial("G4_CELLULOSE_BUTYRATE");
    G4Box* block_shape = new G4Box("Block",14*cm, 14*cm, 7*cm);     //its size
    G4LogicalVolume* block_log = new G4LogicalVolume(block_shape, block_mat, "Block");
    G4ThreeVector block_pos = G4ThreeVector(0,7*cm, 30*cm);
    G4VPhysicalVolume* block = new G4PVPlacement(0, block_pos, "Block", block_log, air, false, 0, checkOverlaps);
    */
    
	
/*
	G4Box* shape = new G4Box("shape", 1*mm,1*mm,1*mm);
	G4LogicalVolume* LV = new G4LogicalVolume(shape,world_mat,"LV");
		G4PVPlacement(0,G4ThreeVector(0,0*cm,0), LV,"PV", NaI_log, false,0,checkOverlaps);
*/
//G4ThreeVector scatterer_pos = G4ThreeVector(0,0,10*cm);
//G4VPhysicalVolume* NaI_scatterer = new G4PVPlacement(0, scatterer_pos, "scatterer", NaI_log, physWorld, false, 0, checkOverlaps);	
//G4VPhysicalVolume* NaI_scatterer2 = new G4PVPlacement(0, G4ThreeVector(0,0,-10*cm), "scatterer", NaI_log, physWorld, false, 1, checkOverlaps);


 //
  //always return the physical World
  //
  return physWorld;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
