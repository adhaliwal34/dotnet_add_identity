# ReadMe

# Overview

The `dotnet_set_up_identity.py` Python script will add basic Identity functionality to a newly minted .NET 10 MVC project created using `dotnet new mvc -o <ProjectName>` e.g. `dotnet new mvc -o MyWebProject`.

The following functionality will be added to the project by the script:
+ A login page
+ A logout link
+ Some text on the home page that will only be seen by logged in users.

The `dotnet_set_up_identity.py` script will:

+ Download various files from a [repo][1] to a temporary directory.
+ Modify the files.
+ Move/copy some files to your new project.
+ Install various required packages to your new project.
+ State next steps required to finish set up.

# Requirements

+ Users must add the Python modules [here][2] to their system in order to run the script.
+ Users must be able to set up a MySQL database to use the login page. Set up and use of the database is beyond the scope of this document.
+ Users must have [Git][3] installed on their systems.
+ Users must have [.NET SDK 10][4] installed on their systems.

# Warning

+ **Note** The project folder files will be modified.
+ The project must be a newly minted MVC project without Identity.
+ **Note** Files that are not normally tracked by version control software e.g. Git are also modified. Currently `appsettings.Development.json`

# Required data

+ `Git_exe` : Path to Git executable including executable name
+ `Dotnet_exe` : Path to dotnet executable including executable name
+ `Temp_dir` : Temp folder. Must exist. (To store a copy of various development files. Can be deleted after use)
+ `Project_name` : Name of the MVC project. Normally can be taken from the `.csproj` file name e.g. `<ProjectName>.csproj`
+ `Project_root_dir` : Directory of your MVC project.
+ `Major_version` : MySQL DB major version (e.g. "8" for "8.0.29)
+ `Minor_version` : MySQL DB minor version (e.g. "0" for "8.0.29)
+ `Patch_version` : MySQL DB patch version (e.g. "29" for "8.0.29)

# How to use

+ Clone this repo.
+ Download these Python modules from [here][2] and make them available for local use.
+ Copy the `demo_dotnet_set_up_identity_settings.json` to `dotnet_set_up_identity_settings.json` and enter the data mentioned in the `Required data` section.
+ Execute `dotnet_set_up_identity.py`.

# The script takes the following steps

## Downloads the VariousDevelopment repo files to a temporary directory

+ Files are from [this public repo][1] and folder `Add_Identity_Asp_dotnet_10`

## Adds <ProjectFolder>/Controllers/AccountsController.cs

+ Moves file to `<ProjectFolder>/Controllers/AccountsController.cs` from the repo.

## Adds <ProjectFolder>/Models/Accounts/AccountLoginViewModel.cs

+ Moves file to `<ProjectFolder>/Models/Accounts/AccountLoginViewModel.cs` from the repo.

## Adds <ProjectFolder>/Data/ApplicationDbContext.cs

+ Moves file to `<ProjectFolder>/Data/ApplicationDbContext.cs` from the repo.

## Adds <ProjectFolder>/Entities/AppUser.cs

+ Moves file to `<ProjectFolder>/Entities/AppUser.cs` from the repo.

## Adds <ProjectFolder>/Views/Accounts/Login.cshtml

+ Moves file to `<ProjectFolder>/Views/Accounts/Login.cshtml` from the repo.

## Modifies <ProjectFolder>/Views/Home/Index.cshtml

+ Add contents from the repo to `<ProjectFolder>/Views/Home/Index.cshtml`.

## Modifies <ProjectFolder>/Views/Shared/_Layout.cshtml

+ Add contents from the repo to `<ProjectFolder>/Views/Shared/_Layout.cshtml`.

## Modifies <ProjectFolder>/appsettings.Development.json

+ Add contents from the repo to `<ProjectFolder>/appsettings.Development.json`.

## Modifies <ProjectFolder>/Program.cs

+ Add contents from the repo to `<ProjectFolder>/Program.cs`.

## Installs packages

+ Installs Microsoft.AspNetCore.Identity.EntityFrameworkCore
+ Installs Pomelo.EntityFrameworkCore.MySql

## States remaining tasks for user

+ Set up MySQL database to use with project with db name and user name given in `appsettings.Development.json`.
+ Set <Server> in `appsettings.Development.json` for MySQL database.
+ Set <Password> in `appsettings.Development.json` for MySQL database.
+ Execute SQL to create various tables required by Identity and add the default app user.

# Creating the Identity tables and a default user in DB

+ Create the seven tables required by the Identity functionality. Order matters:

```sql
CREATE TABLE `AspNetUsers` (
  `Id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UserName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NormalizedUserName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Email` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NormalizedEmail` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EmailConfirmed` tinyint(1) NOT NULL,
  `PasswordHash` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SecurityStamp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ConcurrencyStamp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PhoneNumber` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PhoneNumberConfirmed` tinyint(1) NOT NULL,
  `TwoFactorEnabled` tinyint(1) NOT NULL,
  `LockoutEnd` datetime(6) DEFAULT NULL,
  `LockoutEnabled` tinyint(1) NOT NULL,
  `AccessFailedCount` int NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `UserNameIndex` (`NormalizedUserName`),
  KEY `EmailIndex` (`NormalizedEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetRoles` (
  `Id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NormalizedName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ConcurrencyStamp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `RoleNameIndex` (`NormalizedName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetRoleClaims` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `RoleId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ClaimType` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ClaimValue` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`Id`),
  KEY `IX_AspNetRoleClaims_RoleId` (`RoleId`),
  CONSTRAINT `FK_AspNetRoleClaims_AspNetRoles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `AspNetRoles` (`Id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetUserClaims` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `UserId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ClaimType` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ClaimValue` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`Id`),
  KEY `IX_AspNetUserClaims_UserId` (`UserId`),
  CONSTRAINT `FK_AspNetUserClaims_AspNetUsers_UserId` FOREIGN KEY (`UserId`) REFERENCES `AspNetUsers` (`Id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetUserLogins` (
  `LoginProvider` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProviderKey` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProviderDisplayName` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UserId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`LoginProvider`,`ProviderKey`),
  KEY `IX_AspNetUserLogins_UserId` (`UserId`),
  CONSTRAINT `FK_AspNetUserLogins_AspNetUsers_UserId` FOREIGN KEY (`UserId`) REFERENCES `AspNetUsers` (`Id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetUserRoles` (
  `UserId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RoleId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`UserId`,`RoleId`),
  KEY `IX_AspNetUserRoles_RoleId` (`RoleId`),
  CONSTRAINT `FK_AspNetUserRoles_AspNetRoles_RoleId` FOREIGN KEY (`RoleId`) REFERENCES `AspNetRoles` (`Id`) ON DELETE RESTRICT,
  CONSTRAINT `FK_AspNetUserRoles_AspNetUsers_UserId` FOREIGN KEY (`UserId`) REFERENCES `AspNetUsers` (`Id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `AspNetUserTokens` (
  `UserId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `LoginProvider` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`UserId`,`LoginProvider`,`Name`),
  CONSTRAINT `FK_AspNetUserTokens_AspNetUsers_UserId` FOREIGN KEY (`UserId`) REFERENCES `AspNetUsers` (`Id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

+ Insert app user `test@test.com` password `Abcdefg-1234` directly into DB using the SQL below:

`INSERT INTO `AspNetUsers` VALUES ('8489066c-a444-4348-aeda-445cd9cfa9eb','test@test.com','TEST@TEST.COM','test@test.com','TEST@TEST.COM',1,'AQAAAAIAAYagAAAAEHccuXagKKm7i6POevwP/I/3fnNHwNibsoQOYREWIOpZSRSv3hQsbWeRzb3WUCMoag==','YGKHQEKB2MSXHX6RHJZ2BNRTFKX2UKNR','b153a791-1967-4723-8634-c68c0c2b54a7',NULL,0,0,NULL,1,0);`

[1]: https://github.com/adhaliwal34/VariousDevelopment
[2]: https://github.com/adhaliwal34/aj_python_modules
[3]: https://git-scm.com/
[4]: https://dotnet.microsoft.com/en-us/download