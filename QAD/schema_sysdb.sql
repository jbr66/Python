-- MariaDB dump 10.19  Distrib 10.8.5-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: sysdb
-- ------------------------------------------------------
-- Server version	10.11.4-MariaDB-1:10.11.4+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Sequence structure for `p2j_id_generator_sequence`
--

DROP SEQUENCE IF EXISTS `p2j_id_generator_sequence`;
CREATE SEQUENCE `p2j_id_generator_sequence` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB;
SELECT SETVAL(`p2j_id_generator_sequence`, 2170002, 0);

--
-- Table structure for table `AccessControlEntry`
--

DROP TABLE IF EXISTS `AccessControlEntry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AccessControlEntry` (
  `recid` bigint(20) NOT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `SecurityIdentityID` varchar(64) DEFAULT NULL,
  `Allow` text DEFAULT NULL,
  `Deny` text DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__resourcesecurityindex` (`ResourceURI`,`SecurityIdentityID`),
  KEY `idx__securityid` (`SecurityIdentityID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `AddressType`
--

DROP TABLE IF EXISTS `AddressType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AddressType` (
  `recid` bigint(20) NOT NULL,
  `AddressType_ID` bigint(20) NOT NULL,
  `AddressTypeCode` varchar(20) NOT NULL,
  `AddressTypeDescription` varchar(40) NOT NULL,
  `AddressTypeIsSystemDefined` tinyint(1) NOT NULL,
  `AddressTypeIsActive` tinyint(1) NOT NULL,
  `CustomShort0` varchar(20) DEFAULT NULL,
  `CustomShort1` varchar(20) DEFAULT NULL,
  `CustomShort2` varchar(20) DEFAULT NULL,
  `CustomShort3` varchar(20) DEFAULT NULL,
  `CustomShort4` varchar(20) DEFAULT NULL,
  `CustomShort5` varchar(20) DEFAULT NULL,
  `CustomShort6` varchar(20) DEFAULT NULL,
  `CustomShort7` varchar(20) DEFAULT NULL,
  `CustomShort8` varchar(20) DEFAULT NULL,
  `CustomShort9` varchar(20) DEFAULT NULL,
  `CustomCombo0` varchar(20) DEFAULT NULL,
  `CustomCombo1` varchar(20) DEFAULT NULL,
  `CustomCombo2` varchar(20) DEFAULT NULL,
  `CustomCombo3` varchar(20) DEFAULT NULL,
  `CustomCombo4` varchar(20) DEFAULT NULL,
  `CustomCombo5` varchar(20) DEFAULT NULL,
  `CustomCombo6` varchar(20) DEFAULT NULL,
  `CustomCombo7` varchar(20) DEFAULT NULL,
  `CustomCombo8` varchar(20) DEFAULT NULL,
  `CustomCombo9` varchar(20) DEFAULT NULL,
  `CustomLong0` varchar(255) DEFAULT NULL,
  `CustomLong1` varchar(255) DEFAULT NULL,
  `CustomNote` text DEFAULT NULL,
  `CustomDate0` date DEFAULT NULL,
  `CustomDate1` date DEFAULT NULL,
  `CustomDate2` date DEFAULT NULL,
  `CustomDate3` date DEFAULT NULL,
  `CustomDate4` date DEFAULT NULL,
  `CustomInteger0` int(11) DEFAULT NULL,
  `CustomInteger1` int(11) DEFAULT NULL,
  `CustomInteger2` int(11) DEFAULT NULL,
  `CustomInteger3` int(11) DEFAULT NULL,
  `CustomInteger4` int(11) DEFAULT NULL,
  `CustomDecimal0` decimal(50,4) DEFAULT NULL,
  `CustomDecimal1` decimal(50,4) DEFAULT NULL,
  `CustomDecimal2` decimal(50,4) DEFAULT NULL,
  `CustomDecimal3` decimal(50,4) DEFAULT NULL,
  `CustomDecimal4` decimal(50,4) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`AddressType_ID`),
  UNIQUE KEY `idx__code` (`AddressTypeCode`),
  KEY `idx__lastmodidx` (`LastModifiedDate`,`recid`),
  KEY `idx__viewindex` (`AddressTypeIsActive`,`AddressTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `App`
--

DROP TABLE IF EXISTS `App`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `App` (
  `recid` bigint(20) NOT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `AppName` varchar(200) DEFAULT NULL,
  `Description` varchar(256) DEFAULT NULL,
  `StringCode` varchar(80) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  `IsDefault` tinyint(1) DEFAULT NULL,
  `AppVersion` varchar(32) DEFAULT NULL,
  `QadEnterpriseAppExportVersion` varchar(32) DEFAULT NULL,
  `RegistrationCode` varchar(8) DEFAULT NULL,
  `IsReleased` tinyint(1) DEFAULT NULL,
  `Namespace` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__appidx` (`AppURI`),
  KEY `idx__appname` (`AppName`,`recid`),
  KEY `idx__defaultappidx` (`IsDefault`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `AppDependency`
--

DROP TABLE IF EXISTS `AppDependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AppDependency` (
  `recid` bigint(20) NOT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `DependencyURI` varchar(340) DEFAULT NULL,
  `IsImplicit` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__appdependencyuri` (`AppURI`,`DependencyURI`),
  KEY `idx__dependencyuri` (`DependencyURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `AppModule`
--

DROP TABLE IF EXISTS `AppModule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AppModule` (
  `recid` bigint(20) NOT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__appmoduleidx` (`AppURI`,`ModuleURI`),
  KEY `idx__moduleidx` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ApprovalCfg`
--

DROP TABLE IF EXISTS `ApprovalCfg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ApprovalCfg` (
  `recid` bigint(20) NOT NULL,
  `ApprovalCfgID` varchar(72) DEFAULT NULL,
  `EntityUri` varchar(340) DEFAULT NULL,
  `ApprovalLabel` varchar(80) DEFAULT NULL,
  `ApplicationServiceKey` varchar(80) DEFAULT NULL,
  `ApplicationServiceImpl` varchar(32) DEFAULT NULL,
  `RoutingServiceKey` varchar(80) DEFAULT NULL,
  `RoutingServiceImpl` varchar(32) DEFAULT NULL,
  `ContainerClassName` varchar(200) DEFAULT NULL,
  `ViewMetaUri` varchar(200) DEFAULT NULL,
  `CustomDesktopViewName` varchar(200) DEFAULT NULL,
  `TaskListViewTemplate` varchar(340) DEFAULT NULL,
  `ApproverEmailNotification` tinyint(1) DEFAULT NULL,
  `ApproverInboxNotification` tinyint(1) DEFAULT NULL,
  `ApproverEmailSubject` varchar(400) DEFAULT NULL,
  `ApproverEmailBody` text DEFAULT NULL,
  `StakeholderEmailNotification` tinyint(1) DEFAULT NULL,
  `StakeholderInboxNotification` tinyint(1) DEFAULT NULL,
  `StakeholderEmailSubject` varchar(400) DEFAULT NULL,
  `StakeholderEmailBody` text DEFAULT NULL,
  `EntityRefreshInterval` int(11) DEFAULT NULL,
  `IsEnabled` tinyint(1) DEFAULT NULL,
  `RequireAuthentication` tinyint(1) DEFAULT NULL,
  `EarlyApproval` tinyint(1) DEFAULT NULL,
  `ValidateEntityFields` tinyint(1) DEFAULT NULL,
  `MaximumDetailLines` int(11) DEFAULT NULL,
  `ViewLinkUrl` text DEFAULT NULL,
  `DocumentIdField` varchar(72) DEFAULT NULL,
  `DescriptionField` varchar(72) DEFAULT NULL,
  `CurrencyCodeField` varchar(72) DEFAULT NULL,
  `ExternalLinkUrl` text DEFAULT NULL,
  `TaskColor` varchar(60) DEFAULT NULL,
  `TaskFontIcon` varchar(60) DEFAULT NULL,
  `CombineRoutes` tinyint(1) DEFAULT NULL,
  `AllowNoRoute` tinyint(1) DEFAULT NULL,
  `MassApprovalLabel` varchar(80) DEFAULT NULL,
  `MassApprovalFieldList` varchar(80) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `IsCreatedByWebUI` tinyint(1) DEFAULT NULL,
  `CompletedEntityUri` varchar(340) DEFAULT NULL,
  `CompletedViewLinkUrl` text DEFAULT NULL,
  `RouterEntityUri` varchar(340) DEFAULT NULL,
  `CanSubmitterApprove` tinyint(1) DEFAULT NULL,
  `ActionCallbackEnabled` tinyint(1) DEFAULT NULL,
  `ActionCallbackLastApproverOnly` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__approvalcfgid` (`ApprovalCfgID`),
  UNIQUE KEY `idx__entityuri` (`EntityUri`),
  KEY `idx__approvalcfgmoduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ApprovalCfgFld`
--

DROP TABLE IF EXISTS `ApprovalCfgFld`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ApprovalCfgFld` (
  `recid` bigint(20) NOT NULL,
  `ApprovalCfgFldID` varchar(72) DEFAULT NULL,
  `ApprovalCfgID` varchar(72) DEFAULT NULL,
  `FieldName` varchar(72) DEFAULT NULL,
  `RoutingOption` varchar(64) DEFAULT NULL,
  `DataType` varchar(32) DEFAULT NULL,
  `FieldLabel` varchar(64) DEFAULT NULL,
  `DisplayFormat` varchar(32) DEFAULT NULL,
  `MaxLength` int(11) DEFAULT NULL,
  `MinValue` varchar(64) DEFAULT NULL,
  `MaxValue_` varchar(64) DEFAULT NULL,
  `InputMask` varchar(32) DEFAULT NULL,
  `DataList` varchar(128) DEFAULT NULL,
  `IsRequired` tinyint(1) DEFAULT NULL,
  `State` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__fieldname` (`ApprovalCfgID`,`FieldName`,`RoutingOption`),
  UNIQUE KEY `idx__approvalcfgfldid` (`ApprovalCfgFldID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ApprovalCfgTsk`
--

DROP TABLE IF EXISTS `ApprovalCfgTsk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ApprovalCfgTsk` (
  `recid` bigint(20) NOT NULL,
  `ApprovalCfgTskID` varchar(72) DEFAULT NULL,
  `ApprovalCfgID` varchar(72) DEFAULT NULL,
  `FieldName` varchar(72) DEFAULT NULL,
  `FieldLabel` varchar(64) DEFAULT NULL,
  `FieldCSS` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__fieldname` (`ApprovalCfgID`,`FieldName`),
  UNIQUE KEY `idx__approvalcfgtskid` (`ApprovalCfgTskID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BEBrowse`
--

DROP TABLE IF EXISTS `BEBrowse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BEBrowse` (
  `recid` bigint(20) NOT NULL,
  `BEBrowseURI` varchar(340) DEFAULT NULL,
  `BEBrowseName` varchar(200) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `MetaURI` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  `SearchCondition` text DEFAULT NULL,
  `IsShowCriteriaInSearch` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bebrowseidx` (`BEBrowseURI`),
  KEY `idx__entityuriidx` (`EntityURI`,`recid`),
  KEY `idx__metauriidx` (`MetaURI`,`recid`),
  KEY `idx__moduleidx` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BEBrowseField`
--

DROP TABLE IF EXISTS `BEBrowseField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BEBrowseField` (
  `recid` bigint(20) NOT NULL,
  `BEBrowseFieldID` varchar(72) DEFAULT NULL,
  `BEBrowseURI` varchar(340) DEFAULT NULL,
  `EntityFieldCode` varchar(510) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `SortPosition` int(11) DEFAULT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  `BEBrowseRelationID` varchar(72) DEFAULT NULL,
  `IsFilterOnly` tinyint(1) DEFAULT NULL,
  `IsHiddenFilter` tinyint(1) DEFAULT NULL,
  `IsSortable` tinyint(1) DEFAULT NULL,
  `FieldLabel` varchar(160) DEFAULT NULL,
  `FieldType` text DEFAULT NULL,
  `DisplayFormat` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bebrowsefieldidx` (`BEBrowseFieldID`),
  UNIQUE KEY `idx__bebrowsefielduri` (`BEBrowseURI`,`EntityURI`,`EntityFieldCode`,`BEBrowseRelationID`) USING HASH,
  KEY `idx__bebrowserelationidx` (`BEBrowseRelationID`,`recid`),
  KEY `idx__bebrowseuriidx` (`BEBrowseURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BEBrowseFieldSort`
--

DROP TABLE IF EXISTS `BEBrowseFieldSort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BEBrowseFieldSort` (
  `recid` bigint(20) NOT NULL,
  `BEBrowseURI` varchar(340) DEFAULT NULL,
  `BEBrowseFieldID` varchar(72) DEFAULT NULL,
  `IsDescending` tinyint(1) DEFAULT NULL,
  `SortOrder` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bebrowsefieldidx` (`BEBrowseURI`,`BEBrowseFieldID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BEBrowseRelation`
--

DROP TABLE IF EXISTS `BEBrowseRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BEBrowseRelation` (
  `recid` bigint(20) NOT NULL,
  `BEBrowseRelationID` varchar(72) DEFAULT NULL,
  `ParentBEBrowseRelationID` varchar(72) DEFAULT NULL,
  `BEBrowseURI` varchar(340) DEFAULT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  `RelatedEntityURI` varchar(340) DEFAULT NULL,
  `JoinType` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__browserelationidx` (`BEBrowseRelationID`),
  KEY `idx__berelationidx` (`RelationID`,`recid`),
  KEY `idx__browseuriidx` (`BEBrowseURI`,`recid`),
  KEY `idx__parentbrowserelationidx` (`ParentBEBrowseRelationID`,`recid`),
  KEY `idx__relatedbeidx` (`RelatedEntityURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BERelation`
--

DROP TABLE IF EXISTS `BERelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BERelation` (
  `recid` bigint(20) NOT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  `RelationCode` varchar(256) DEFAULT NULL,
  `RelationLabel` varchar(160) DEFAULT NULL,
  `SourceEntityCode` varchar(160) DEFAULT NULL,
  `SourceEntityURI` varchar(340) DEFAULT NULL,
  `RelatedEntityCode` varchar(160) DEFAULT NULL,
  `RelatedEntityURI` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `Cardinality` varchar(340) DEFAULT NULL,
  `IsDrill` tinyint(1) DEFAULT NULL,
  `IsLookup` tinyint(1) DEFAULT NULL,
  `IsParent` tinyint(1) DEFAULT NULL,
  `IsEmbedded` tinyint(1) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `IsExtension` tinyint(1) DEFAULT NULL,
  `IsCascadeDelete` tinyint(1) DEFAULT NULL,
  `MasterField` varchar(510) DEFAULT NULL,
  `RelationType` varchar(80) DEFAULT NULL,
  `RelatedAppURI` varchar(340) DEFAULT NULL,
  `IsVisualizedAsDropDown` tinyint(1) DEFAULT NULL,
  `FieldUsedForLabel` varchar(510) DEFAULT NULL,
  `LookupResource` varchar(510) DEFAULT NULL,
  `IsIncludeOnParent` tinyint(1) DEFAULT NULL,
  `IsUseInBusinessDocument` tinyint(1) DEFAULT NULL,
  `IsCascadeDeleteForBD` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__relationid` (`RelationID`),
  KEY `idx__cardinality` (`Cardinality`,`recid`),
  KEY `idx__isextension` (`IsExtension`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__relatedentityuri` (`RelatedEntityURI`,`recid`),
  KEY `idx__relationcodeidx` (`RelationCode`,`recid`),
  KEY `idx__sourceentityuri` (`SourceEntityURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BERelationField`
--

DROP TABLE IF EXISTS `BERelationField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BERelationField` (
  `recid` bigint(20) NOT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  `SourceFieldCode` varchar(510) DEFAULT NULL,
  `RelatedFieldCode` varchar(510) DEFAULT NULL,
  `SourceFieldParentTable` varchar(200) DEFAULT NULL,
  `RelatedFieldParentTable` varchar(200) DEFAULT NULL,
  `SourceFieldLiteral` varchar(510) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__relationfield` (`RelationID`,`SourceFieldCode`,`RelatedFieldCode`) USING HASH,
  KEY `idx__relationididx` (`RelationID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BERelationFilterCondition`
--

DROP TABLE IF EXISTS `BERelationFilterCondition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BERelationFilterCondition` (
  `recid` bigint(20) NOT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  `FieldName` varchar(120) DEFAULT NULL,
  `Operator` varchar(24) DEFAULT NULL,
  `FieldValue1` varchar(120) DEFAULT NULL,
  `FieldValue2` varchar(120) DEFAULT NULL,
  `DataType` varchar(32) DEFAULT NULL,
  `FieldName2` varchar(120) DEFAULT NULL,
  `EntityURI1` varchar(340) DEFAULT NULL,
  `EntityURI2` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__relationfiltercondition` (`RelationID`,`FieldName`,`FieldValue1`,`FieldValue2`,`FieldName2`,`EntityURI1`,`EntityURI2`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BankAccFormat`
--

DROP TABLE IF EXISTS `BankAccFormat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BankAccFormat` (
  `recid` bigint(20) NOT NULL,
  `BankAccFormat_ID` bigint(20) NOT NULL,
  `BankAccFormatCode` varchar(20) NOT NULL,
  `BankAccFormatDescription` varchar(40) NOT NULL,
  `BankAccFormatIsSystDefined` tinyint(1) NOT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`BankAccFormat_ID`),
  UNIQUE KEY `idx__uniqueidx` (`BankAccFormatCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BankAccFormatSect`
--

DROP TABLE IF EXISTS `BankAccFormatSect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BankAccFormatSect` (
  `recid` bigint(20) NOT NULL,
  `BankAccFormatSect_ID` bigint(20) NOT NULL,
  `BankAccFormat_ID` bigint(20) NOT NULL,
  `BankAccFormatSectSequence` int(11) NOT NULL,
  `BankAccFormatSectLabel` varchar(40) DEFAULT NULL,
  `BankAccFormatSectLength` int(11) DEFAULT NULL,
  `BankAccFormatSectIsMandat` tinyint(1) NOT NULL,
  `BankAccFormatSectIsLdZero` tinyint(1) NOT NULL,
  `BankAccFormatSectDelimiter` varchar(1) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__uniqueidx` (`BankAccFormat_ID`,`BankAccFormatSectSequence`),
  UNIQUE KEY `idx__prim` (`BankAccFormatSect_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Bdocument`
--

DROP TABLE IF EXISTS `Bdocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Bdocument` (
  `recid` bigint(20) NOT NULL,
  `BdocumentID` varchar(160) DEFAULT NULL,
  `BdocumentURI` varchar(340) DEFAULT NULL,
  `BdocumentCode` varchar(64) DEFAULT NULL,
  `BdocumentLabel` varchar(64) DEFAULT NULL,
  `RootComponentURI` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `Organization` varchar(32) DEFAULT NULL,
  `Application` varchar(32) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `BdocumentDescription` text DEFAULT NULL,
  `BdocumentBrowseURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bdocumenturi` (`BdocumentURI`),
  UNIQUE KEY `idx__bdocumentid` (`BdocumentID`),
  KEY `idx__bdocumentcode` (`BdocumentCode`,`recid`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__rootcomponenturi` (`RootComponentURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BdocumentCom`
--

DROP TABLE IF EXISTS `BdocumentCom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BdocumentCom` (
  `recid` bigint(20) NOT NULL,
  `BdocumentComID` varchar(160) DEFAULT NULL,
  `BdocumentID` varchar(340) DEFAULT NULL,
  `BusinessComponentURI` varchar(340) DEFAULT NULL,
  `Identifier` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bdocumentcomid` (`BdocumentComID`),
  KEY `idx__bdocumentid` (`BdocumentID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BdocumentRel`
--

DROP TABLE IF EXISTS `BdocumentRel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BdocumentRel` (
  `recid` bigint(20) NOT NULL,
  `BdocumentRelID` varchar(160) DEFAULT NULL,
  `BdocumentID` varchar(340) DEFAULT NULL,
  `ParentComponentURI` varchar(340) DEFAULT NULL,
  `ChildComponentURI` varchar(340) DEFAULT NULL,
  `RelationID` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__bdocumentrelid` (`BdocumentRelID`),
  KEY `idx__bdocumentid` (`BdocumentID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Document`
--

DROP TABLE IF EXISTS `Document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Document` (
  `recid` bigint(20) NOT NULL,
  `Key_` varchar(144) DEFAULT NULL,
  `Content` mediumtext DEFAULT NULL,
  `ContentUtf8` mediumtext DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__documentindex` (`Key_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityDataList`
--

DROP TABLE IF EXISTS `EntityDataList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityDataList` (
  `recid` bigint(20) NOT NULL,
  `EntityDataListID` varchar(72) DEFAULT NULL,
  `DataListCode` varchar(128) DEFAULT NULL,
  `ServiceCall` varchar(510) DEFAULT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entitydatalistid` (`EntityDataListID`),
  KEY `idx__entityid` (`EntityID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityDataListValue`
--

DROP TABLE IF EXISTS `EntityDataListValue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityDataListValue` (
  `recid` bigint(20) NOT NULL,
  `EntityDataListValueID` varchar(72) DEFAULT NULL,
  `EntityDataListID` varchar(72) DEFAULT NULL,
  `DataLabel` varchar(160) DEFAULT NULL,
  `DataValue` varchar(160) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `DataOrder` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entitydatalistvalueid` (`EntityDataListValueID`),
  KEY `idx__datalistindex` (`EntityDataListID`,`DataLabel`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityField`
--

DROP TABLE IF EXISTS `EntityField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityField` (
  `recid` bigint(20) NOT NULL,
  `EntityFieldID` varchar(72) DEFAULT NULL,
  `EntityTableID` varchar(72) DEFAULT NULL,
  `EntityFieldCode` varchar(510) DEFAULT NULL,
  `FieldLabel` varchar(160) DEFAULT NULL,
  `FieldDescription` varchar(510) DEFAULT NULL,
  `IsRequired` tinyint(1) DEFAULT NULL,
  `IsReadOnly` tinyint(1) DEFAULT NULL,
  `DataType` varchar(32) DEFAULT NULL,
  `ValidationPattern` varchar(64) DEFAULT NULL,
  `HelpID` varchar(160) DEFAULT NULL,
  `DisplayFormat` varchar(160) DEFAULT NULL,
  `DefaultValue` varchar(32) DEFAULT NULL,
  `MaxLength` int(11) DEFAULT NULL,
  `MinValue` varchar(64) DEFAULT NULL,
  `MaxValue_` varchar(64) DEFAULT NULL,
  `InputMask` varchar(32) DEFAULT NULL,
  `EntityDataListID` varchar(72) DEFAULT NULL,
  `LookupCode` varchar(128) DEFAULT NULL,
  `LookupResultField` varchar(128) DEFAULT NULL,
  `LookupSearchField` varchar(128) DEFAULT NULL,
  `FieldGroup` varchar(64) DEFAULT NULL,
  `JsonName` varchar(160) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `IsUserDefinedField` tinyint(1) DEFAULT NULL,
  `OverrideContextType` varchar(64) DEFAULT NULL,
  `IsFollowable` tinyint(1) DEFAULT NULL,
  `IsSortable` tinyint(1) DEFAULT NULL,
  `IsDeployed` tinyint(1) DEFAULT NULL,
  `PhysicalFieldName` varchar(510) DEFAULT NULL,
  `IsHidden` tinyint(1) DEFAULT NULL,
  `IsImported` tinyint(1) DEFAULT NULL,
  `AssociatedField` varchar(510) DEFAULT NULL,
  `IsDiscriminator` tinyint(1) DEFAULT NULL,
  `IsFormula` tinyint(1) DEFAULT NULL,
  `Formula` mediumtext DEFAULT NULL,
  `CurrencyField` varchar(510) DEFAULT NULL,
  `SubDataType` varchar(32) DEFAULT NULL,
  `IsExcludedFromConcurrencyHash` tinyint(1) DEFAULT NULL,
  `IsHiddenForUI` tinyint(1) DEFAULT NULL,
  `TranslationType` varchar(64) DEFAULT NULL,
  `FormattedBy` varchar(510) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entityfieldid` (`EntityFieldID`),
  KEY `idx__entityfieldcode` (`EntityFieldCode`,`recid`),
  KEY `idx__entitytableid` (`EntityTableID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityFieldGroup`
--

DROP TABLE IF EXISTS `EntityFieldGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityFieldGroup` (
  `recid` bigint(20) NOT NULL,
  `EntityFieldGroupID` varchar(72) DEFAULT NULL,
  `FieldGroupCode` varchar(128) DEFAULT NULL,
  `FieldGroupLabel` varchar(510) DEFAULT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entityfieldgroupid` (`EntityFieldGroupID`),
  KEY `idx__entityid` (`EntityID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityFieldLookupSearchCondn`
--

DROP TABLE IF EXISTS `EntityFieldLookupSearchCondn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityFieldLookupSearchCondn` (
  `recid` bigint(20) NOT NULL,
  `EntityFieldLookupSearchCondnID` varchar(72) DEFAULT NULL,
  `EntityFieldID` varchar(72) DEFAULT NULL,
  `FieldName` varchar(72) DEFAULT NULL,
  `Operator` varchar(72) DEFAULT NULL,
  `FieldValue` varchar(128) DEFAULT NULL,
  `FieldValueType` varchar(48) DEFAULT NULL,
  `FieldValue2` varchar(128) DEFAULT NULL,
  `FieldValue2Type` varchar(48) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entityfieldlookupsearchcondnid` (`EntityFieldLookupSearchCondnID`),
  UNIQUE KEY `idx__entityfieldlookupsearchcondn` (`EntityFieldID`,`FieldName`,`Operator`,`FieldValue`,`FieldValue2`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityFieldOverride`
--

DROP TABLE IF EXISTS `EntityFieldOverride`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityFieldOverride` (
  `recid` bigint(20) NOT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `BusinessEntityURI` varchar(340) DEFAULT NULL,
  `EntityFieldCode` varchar(510) DEFAULT NULL,
  `ContextType` varchar(64) DEFAULT NULL,
  `ContextValue` varchar(128) DEFAULT NULL,
  `PropertyName` varchar(128) DEFAULT NULL,
  `PropertyValue` text DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  `Note` varchar(510) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__moduleentityfieldcontextproperty` (`ModuleURI`,`BusinessEntityURI`,`EntityFieldCode`,`ContextType`,`ContextValue`,`PropertyName`) USING HASH,
  KEY `idx__entitycontext` (`BusinessEntityURI`,`ContextType`,`ContextValue`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityMapping`
--

DROP TABLE IF EXISTS `EntityMapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityMapping` (
  `recid` bigint(20) NOT NULL,
  `EntityMappingID` varchar(72) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `RootSourceTable` varchar(72) DEFAULT NULL,
  `RootSourceTableKeyFields` varchar(510) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `MappingXML` mediumtext DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entityuri` (`EntityURI`),
  UNIQUE KEY `idx__entitymappingid` (`EntityMappingID`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__rootsourcetable` (`RootSourceTable`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityMetadata`
--

DROP TABLE IF EXISTS `EntityMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityMetadata` (
  `recid` bigint(20) NOT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `ModuleName` varchar(64) DEFAULT NULL,
  `EntityCode` varchar(80) DEFAULT NULL,
  `EntityDescription` varchar(510) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `EntityName` varchar(160) DEFAULT NULL,
  `Extends` varchar(120) DEFAULT NULL,
  `IsFollowable` tinyint(1) DEFAULT NULL,
  `Scope` varchar(64) DEFAULT NULL,
  `IsDataExtensionOnly` tinyint(1) DEFAULT NULL,
  `IsAllowApproval` tinyint(1) DEFAULT NULL,
  `IsBusinessDocument` tinyint(1) DEFAULT NULL,
  `IsUseOptimisticLocking` tinyint(1) DEFAULT NULL,
  `BusinessComponentStatus` varchar(20) DEFAULT NULL,
  `DraftIDField` varchar(510) DEFAULT NULL,
  `SharedSetType` varchar(64) DEFAULT NULL,
  `SecureResourceURI` varchar(340) DEFAULT NULL,
  `DoNotExtend` tinyint(1) DEFAULT NULL,
  `DoNotExtendReason` varchar(360) DEFAULT NULL,
  `TransCommentsField` varchar(510) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entityid` (`EntityID`),
  KEY `idx__businesscomponentstatusindex` (`BusinessComponentStatus`,`recid`),
  KEY `idx__entityindex` (`EntityCode`,`ModuleName`,`recid`),
  KEY `idx__entityuri` (`EntityURI`,`recid`),
  KEY `idx__extendsindex` (`Extends`,`recid`),
  KEY `idx__modulename` (`ModuleName`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__secureresourceuri` (`SecureResourceURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityRelationship`
--

DROP TABLE IF EXISTS `EntityRelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityRelationship` (
  `recid` bigint(20) NOT NULL,
  `EntityRelationshipID` varchar(72) DEFAULT NULL,
  `ParentEntityTableCode` varchar(160) DEFAULT NULL,
  `ChildEntityTableCode` varchar(160) DEFAULT NULL,
  `ParentFields` varchar(510) DEFAULT NULL,
  `ChildFields` varchar(510) DEFAULT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `Cardinality` varchar(20) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  KEY `idx__entityid` (`EntityID`,`recid`),
  KEY `idx__entityrelationshipid` (`EntityRelationshipID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EntityTable`
--

DROP TABLE IF EXISTS `EntityTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EntityTable` (
  `recid` bigint(20) NOT NULL,
  `EntityTableID` varchar(72) DEFAULT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `EntityTableCode` varchar(160) DEFAULT NULL,
  `TableDescription` varchar(510) DEFAULT NULL,
  `TableKeyFields` varchar(510) DEFAULT NULL,
  `JsonName` varchar(160) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__entitytableid` (`EntityTableID`),
  KEY `idx__entityid` (`EntityID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EventHandler`
--

DROP TABLE IF EXISTS `EventHandler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EventHandler` (
  `recid` bigint(20) NOT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `ViewURI` varchar(340) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `EventHandlerType` varchar(16) DEFAULT NULL,
  `JavaScriptCode` mediumtext DEFAULT NULL,
  `TypeScriptCode` mediumtext DEFAULT NULL,
  `MappingCode` mediumtext DEFAULT NULL,
  `Properties` mediumtext DEFAULT NULL,
  `AppliesTo` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__appviewtypeapplies` (`AppURI`,`ViewURI`,`EventHandlerType`,`AppliesTo`),
  KEY `idx__viewuri` (`ViewURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EventTypeRegistry`
--

DROP TABLE IF EXISTS `EventTypeRegistry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EventTypeRegistry` (
  `recid` bigint(20) NOT NULL,
  `EventTypeRegistryID` varchar(72) DEFAULT NULL,
  `RegistryName` varchar(200) DEFAULT NULL,
  `TableName` varchar(200) DEFAULT NULL,
  `Filter` text DEFAULT NULL,
  `EventName` varchar(64) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `FieldList` text DEFAULT NULL,
  `SaveAllFields` tinyint(1) DEFAULT NULL,
  `ParentEvent` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__registeredeventtype` (`RegistryName`,`TableName`,`EventName`),
  UNIQUE KEY `idx__registryid` (`EventTypeRegistryID`),
  KEY `idx__eventtable` (`EventName`,`TableName`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ExchangeRateType`
--

DROP TABLE IF EXISTS `ExchangeRateType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ExchangeRateType` (
  `recid` bigint(20) NOT NULL,
  `ExchangeRateType_ID` bigint(20) NOT NULL,
  `ExchangeRateTypeCode` varchar(20) NOT NULL,
  `ExchangeRateTypeDescript` varchar(40) NOT NULL,
  `ExchangeRateTypeIsSystem` tinyint(1) NOT NULL,
  `ExchangeRateTypeIsActive` tinyint(1) NOT NULL,
  `ExchangeRateTypeIsExported` tinyint(1) NOT NULL,
  `CustomShort0` varchar(20) DEFAULT NULL,
  `CustomShort1` varchar(20) DEFAULT NULL,
  `CustomShort2` varchar(20) DEFAULT NULL,
  `CustomShort3` varchar(20) DEFAULT NULL,
  `CustomShort4` varchar(20) DEFAULT NULL,
  `CustomShort5` varchar(20) DEFAULT NULL,
  `CustomShort6` varchar(20) DEFAULT NULL,
  `CustomShort7` varchar(20) DEFAULT NULL,
  `CustomShort8` varchar(20) DEFAULT NULL,
  `CustomShort9` varchar(20) DEFAULT NULL,
  `CustomCombo0` varchar(20) DEFAULT NULL,
  `CustomCombo1` varchar(20) DEFAULT NULL,
  `CustomCombo2` varchar(20) DEFAULT NULL,
  `CustomCombo3` varchar(20) DEFAULT NULL,
  `CustomCombo4` varchar(20) DEFAULT NULL,
  `CustomCombo5` varchar(20) DEFAULT NULL,
  `CustomCombo6` varchar(20) DEFAULT NULL,
  `CustomCombo7` varchar(20) DEFAULT NULL,
  `CustomCombo8` varchar(20) DEFAULT NULL,
  `CustomCombo9` varchar(20) DEFAULT NULL,
  `CustomLong0` varchar(255) DEFAULT NULL,
  `CustomLong1` varchar(255) DEFAULT NULL,
  `CustomNote` text DEFAULT NULL,
  `CustomDate0` date DEFAULT NULL,
  `CustomDate1` date DEFAULT NULL,
  `CustomDate2` date DEFAULT NULL,
  `CustomDate3` date DEFAULT NULL,
  `CustomDate4` date DEFAULT NULL,
  `CustomInteger0` int(11) DEFAULT NULL,
  `CustomInteger1` int(11) DEFAULT NULL,
  `CustomInteger2` int(11) DEFAULT NULL,
  `CustomInteger3` int(11) DEFAULT NULL,
  `CustomInteger4` int(11) DEFAULT NULL,
  `CustomDecimal0` decimal(50,4) DEFAULT NULL,
  `CustomDecimal1` decimal(50,4) DEFAULT NULL,
  `CustomDecimal2` decimal(50,4) DEFAULT NULL,
  `CustomDecimal3` decimal(50,4) DEFAULT NULL,
  `CustomDecimal4` decimal(50,4) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `ExchangeRateTypeIsFallBack` tinyint(1) NOT NULL,
  `ExchangeRateTypeIsTillDate` tinyint(1) NOT NULL,
  `ExchangeRateTypeValidity` int(11) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`ExchangeRateType_ID`),
  UNIQUE KEY `idx__code` (`ExchangeRateTypeCode`),
  KEY `idx__viewindex` (`ExchangeRateTypeIsActive`,`ExchangeRateTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `FieldSecurityPattern`
--

DROP TABLE IF EXISTS `FieldSecurityPattern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FieldSecurityPattern` (
  `recid` bigint(20) NOT NULL,
  `FieldSecurityPatternID` varchar(72) NOT NULL,
  `PatternType` varchar(16) NOT NULL,
  `PatternValue` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__patternid` (`FieldSecurityPatternID`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__patterntype` (`PatternType`,`recid`),
  KEY `idx__patternvalue` (`PatternValue`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `FormulaFieldInfo`
--

DROP TABLE IF EXISTS `FormulaFieldInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FormulaFieldInfo` (
  `recid` bigint(20) NOT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `TableName` varchar(64) DEFAULT NULL,
  `FieldName` varchar(80) DEFAULT NULL,
  `FormulaAppURI` varchar(340) DEFAULT NULL,
  `FormulaEntityURI` varchar(340) DEFAULT NULL,
  `FormulaTableName` varchar(64) DEFAULT NULL,
  `FormulaFieldName` varchar(80) DEFAULT NULL,
  `RelationPath` text DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__formulafieldinfoidx` (`EntityURI`,`TableName`,`FieldName`,`FormulaAppURI`,`FormulaEntityURI`,`FormulaTableName`,`FormulaFieldName`,`RelationPath`) USING HASH,
  KEY `idx__formulaappuriidx` (`FormulaAppURI`,`recid`),
  KEY `idx__formulaentityuriidx` (`FormulaEntityURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GLSystemType`
--

DROP TABLE IF EXISTS `GLSystemType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GLSystemType` (
  `recid` bigint(20) NOT NULL,
  `GLSystemTypeCode` varchar(20) NOT NULL,
  `GLSystemTypeTranslated` varchar(20) DEFAULT NULL,
  `GLSystemTypeIsActive` tinyint(1) NOT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`GLSystemTypeCode`),
  KEY `idx__active` (`GLSystemTypeIsActive`,`recid`),
  KEY `idx__viewindex` (`GLSystemTypeIsActive`,`GLSystemTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GLType`
--

DROP TABLE IF EXISTS `GLType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GLType` (
  `recid` bigint(20) NOT NULL,
  `GLTypeCode` varchar(20) NOT NULL,
  `GLTypeIsActive` tinyint(1) NOT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`GLTypeCode`),
  KEY `idx__viewindex` (`GLTypeIsActive`,`GLTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IndexFieldMetadata`
--

DROP TABLE IF EXISTS `IndexFieldMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IndexFieldMetadata` (
  `recid` bigint(20) NOT NULL,
  `IndexID` varchar(128) NOT NULL,
  `FieldName` varchar(64) NOT NULL,
  `SequenceNumber` int(11) DEFAULT NULL,
  `IsAscending` tinyint(1) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__idx_pk` (`IndexID`,`FieldName`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDatetime`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IndexMetadata`
--

DROP TABLE IF EXISTS `IndexMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IndexMetadata` (
  `recid` bigint(20) NOT NULL,
  `IndexID` varchar(128) NOT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `IndexName` varchar(64) NOT NULL,
  `IsUnique` tinyint(1) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `IsPrimary` tinyint(1) DEFAULT NULL,
  `ProDescription` varchar(180) DEFAULT NULL,
  `IsDeployed` tinyint(1) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__idx_pk` (`IndexID`),
  UNIQUE KEY `idx__idx_uniquename` (`EntityURI`,`IndexName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `JournalType`
--

DROP TABLE IF EXISTS `JournalType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `JournalType` (
  `recid` bigint(20) NOT NULL,
  `JournalTypeCode` varchar(30) NOT NULL,
  `JournalTypeIsActive` tinyint(1) NOT NULL,
  `JournalTypeIsMultiJournal` tinyint(1) DEFAULT NULL,
  `JournalTypeIsAllowOfficial` tinyint(1) NOT NULL,
  `JournalTypeIsAllowMgt` tinyint(1) NOT NULL,
  `JournalTypeIsAllowTrans` tinyint(1) NOT NULL,
  `JournalTypeIsStock` tinyint(1) NOT NULL,
  `JournalTypeIsCorrection` tinyint(1) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`JournalTypeCode`),
  KEY `idx__viewindex` (`JournalTypeIsActive`,`JournalTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `KpiMetaDomain`
--

DROP TABLE IF EXISTS `KpiMetaDomain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KpiMetaDomain` (
  `recid` bigint(20) NOT NULL,
  `KpiCode` varchar(64) DEFAULT NULL,
  `KpiMetaDomainID` int(11) DEFAULT NULL,
  `Domain` varchar(120) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__codeid` (`KpiCode`,`KpiMetaDomainID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `KpiMetaEntity`
--

DROP TABLE IF EXISTS `KpiMetaEntity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KpiMetaEntity` (
  `recid` bigint(20) NOT NULL,
  `KpiCode` varchar(64) DEFAULT NULL,
  `KpiMetaEntityID` int(11) DEFAULT NULL,
  `Entity` varchar(120) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__codeid` (`KpiCode`,`KpiMetaEntityID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `KpiMetaField`
--

DROP TABLE IF EXISTS `KpiMetaField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KpiMetaField` (
  `recid` bigint(20) NOT NULL,
  `KpiCode` varchar(64) DEFAULT NULL,
  `FieldName` varchar(128) DEFAULT NULL,
  `LogiFieldName` varchar(128) DEFAULT NULL,
  `FieldLabel` varchar(64) DEFAULT NULL,
  `DataType` varchar(24) DEFAULT NULL,
  `CurrencyType` varchar(64) DEFAULT NULL,
  `FieldFormat` varchar(48) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `IsCompare` tinyint(1) DEFAULT NULL,
  `IsSum` tinyint(1) DEFAULT NULL,
  `IsGroupBy` tinyint(1) DEFAULT NULL,
  `HasPopupValuesForFilter` tinyint(1) DEFAULT NULL,
  `Aggregation` varchar(48) DEFAULT NULL,
  `CaseType` varchar(48) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__codefield` (`KpiCode`,`FieldName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `KpiMetaFilter`
--

DROP TABLE IF EXISTS `KpiMetaFilter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KpiMetaFilter` (
  `recid` bigint(20) NOT NULL,
  `KpiCode` varchar(64) DEFAULT NULL,
  `KpiMetaFilterID` int(11) DEFAULT NULL,
  `FieldName` varchar(120) DEFAULT NULL,
  `Operator` varchar(24) DEFAULT NULL,
  `Value1` varchar(120) DEFAULT NULL,
  `Value2` varchar(120) DEFAULT NULL,
  `Value1Type` varchar(24) DEFAULT NULL,
  `Value2Type` varchar(24) DEFAULT NULL,
  `FieldLabel` varchar(64) DEFAULT NULL,
  `OperatorLabel` varchar(64) DEFAULT NULL,
  `Value1Label` varchar(64) DEFAULT NULL,
  `Value2Label` varchar(64) DEFAULT NULL,
  `EditLogicString` text DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__codeid` (`KpiCode`,`KpiMetaFilterID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `KpiMetadata`
--

DROP TABLE IF EXISTS `KpiMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KpiMetadata` (
  `recid` bigint(20) NOT NULL,
  `KpiCode` varchar(64) DEFAULT NULL,
  `DataSourceType` varchar(64) DEFAULT NULL,
  `DataSource` varchar(340) DEFAULT NULL,
  `DataSourceLabel` varchar(64) DEFAULT NULL,
  `AutoRefresh` tinyint(1) DEFAULT NULL,
  `RefreshRate` varchar(32) DEFAULT NULL,
  `AllowManualRefresh` tinyint(1) DEFAULT NULL,
  `NumPeriods` varchar(8) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `CurrentWorkspaceOnly` tinyint(1) DEFAULT NULL,
  `BrowseByDomain` tinyint(1) DEFAULT NULL,
  `BrowseByEntity` tinyint(1) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `ViewProvider` varchar(80) DEFAULT NULL,
  `KpiName` varchar(256) DEFAULT NULL,
  `GroupDatesBy` varchar(48) DEFAULT NULL,
  `GroupData` tinyint(1) DEFAULT NULL,
  `KpiType` varchar(48) DEFAULT NULL,
  `HasHistoricalSnapshot` tinyint(1) DEFAULT NULL,
  `SnapshotRate` varchar(48) DEFAULT NULL,
  `SnapshotSchedule` varchar(20) DEFAULT NULL,
  `SnapshotScheduleTime` timestamp(3) NULL DEFAULT NULL,
  `SnapshotScheduleTime_offset` int(11) DEFAULT NULL,
  `SnapshotRetention` int(11) DEFAULT NULL,
  `SnapshotScheduleTimezone` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__kpicode` (`KpiCode`),
  KEY `idx__autorefresh` (`AutoRefresh`,`recid`),
  KEY `idx__isactive` (`IsActive`,`recid`),
  KEY `idx__kpiname` (`KpiName`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__viewprovider` (`ViewProvider`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Layout`
--

DROP TABLE IF EXISTS `Layout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Layout` (
  `recid` bigint(20) NOT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `ViewURI` varchar(340) DEFAULT NULL,
  `LayoutName` varchar(128) DEFAULT NULL,
  `Description` varchar(256) DEFAULT NULL,
  `ContextType` varchar(64) DEFAULT NULL,
  `ContextValue` varchar(128) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `LayoutData` mediumtext DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__moduleviewlayout` (`ModuleURI`,`ViewURI`,`LayoutName`) USING HASH,
  KEY `idx__layoutname` (`LayoutName`,`recid`),
  KEY `idx__viewuri` (`ViewURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Locale`
--

DROP TABLE IF EXISTS `Locale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locale` (
  `recid` bigint(20) NOT NULL,
  `LocaleID` varchar(72) NOT NULL,
  `LanguageCode` varchar(4) NOT NULL,
  `RegionCode` varchar(4) NOT NULL,
  `Description` varchar(48) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `IsInstalled` tinyint(1) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `MfgLanguageCode` varchar(16) DEFAULT NULL,
  `DateFormat` varchar(32) DEFAULT NULL,
  `DateTimeFormat` varchar(50) DEFAULT NULL,
  `NumericalFormat` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__localeid` (`LocaleID`),
  UNIQUE KEY `idx__alternate` (`LanguageCode`,`RegionCode`),
  KEY `idx__mfglanguage` (`MfgLanguageCode`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LookupDefinition`
--

DROP TABLE IF EXISTS `LookupDefinition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LookupDefinition` (
  `recid` bigint(20) NOT NULL,
  `FieldSet` varchar(340) DEFAULT NULL,
  `Reference` varchar(340) DEFAULT NULL,
  `BrowseURI` varchar(340) DEFAULT NULL,
  `ResultField` varchar(128) DEFAULT NULL,
  `SearchField` varchar(128) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `SearchFieldOperator` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lookupdefinition` (`ModuleURI`,`FieldSet`,`Reference`) USING HASH,
  KEY `idx__fieldset` (`FieldSet`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LookupQualifier`
--

DROP TABLE IF EXISTS `LookupQualifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LookupQualifier` (
  `recid` bigint(20) NOT NULL,
  `FieldSet` varchar(340) DEFAULT NULL,
  `Reference` varchar(340) DEFAULT NULL,
  `QualifierType` varchar(32) DEFAULT NULL,
  `QualifierName` varchar(510) DEFAULT NULL,
  `QualifierValue` varchar(510) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lookupqualifier` (`ModuleURI`,`FieldSet`,`Reference`,`QualifierType`,`QualifierName`,`QualifierValue`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LookupResultField`
--

DROP TABLE IF EXISTS `LookupResultField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LookupResultField` (
  `recid` bigint(20) NOT NULL,
  `FieldSet` varchar(340) DEFAULT NULL,
  `Reference` varchar(340) DEFAULT NULL,
  `ResultField` varchar(128) DEFAULT NULL,
  `TargetFieldSet` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lookupresultfield` (`ModuleURI`,`FieldSet`,`Reference`,`ResultField`,`TargetFieldSet`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LookupSearchCondition`
--

DROP TABLE IF EXISTS `LookupSearchCondition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LookupSearchCondition` (
  `recid` bigint(20) NOT NULL,
  `FieldSet` varchar(340) DEFAULT NULL,
  `Reference` varchar(340) DEFAULT NULL,
  `FieldName` varchar(72) DEFAULT NULL,
  `Operator` varchar(72) DEFAULT NULL,
  `FieldValue1` varchar(128) DEFAULT NULL,
  `FieldValue1Type` varchar(48) DEFAULT NULL,
  `FieldValue2` varchar(128) DEFAULT NULL,
  `FieldValue2Type` varchar(48) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lookupsearchcondition` (`ModuleURI`,`FieldSet`,`Reference`,`FieldName`,`Operator`,`FieldValue1`,`FieldValue2`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MenuResource`
--

DROP TABLE IF EXISTS `MenuResource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MenuResource` (
  `recid` bigint(20) NOT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__resourceuri` (`ResourceURI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MenuTree`
--

DROP TABLE IF EXISTS `MenuTree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MenuTree` (
  `recid` bigint(20) NOT NULL,
  `MenuTreeID` varchar(72) DEFAULT NULL,
  `MenuType` varchar(128) DEFAULT NULL,
  `MenuCode` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__logicalkey` (`MenuType`,`MenuCode`),
  KEY `idx__menutreeid` (`MenuTreeID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MenuTreeNode`
--

DROP TABLE IF EXISTS `MenuTreeNode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MenuTreeNode` (
  `recid` bigint(20) NOT NULL,
  `MenuTreeNodeID` varchar(72) DEFAULT NULL,
  `MenuTreeID` varchar(72) DEFAULT NULL,
  `Path` varchar(256) DEFAULT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `StringCode` varchar(80) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `IncludeInMobile` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__idx2` (`MenuTreeID`,`Path`,`ResourceURI`),
  UNIQUE KEY `idx__menutreenodeid` (`MenuTreeNodeID`),
  KEY `idx__menutreeid` (`MenuTreeID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NotifyCateg`
--

DROP TABLE IF EXISTS `NotifyCateg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NotifyCateg` (
  `recid` bigint(20) NOT NULL,
  `NotifyCategID` varchar(72) DEFAULT NULL,
  `CategoryName` varchar(60) DEFAULT NULL,
  `UsrID` varchar(32) DEFAULT NULL,
  `ReceiveNotification` varchar(2) DEFAULT NULL,
  `InboxNotification` varchar(2) DEFAULT NULL,
  `EmailNotification` varchar(2) DEFAULT NULL,
  `DisabledNotifications` varchar(72) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__notifycategid` (`NotifyCategID`),
  UNIQUE KEY `idx__categoryname` (`UsrID`,`CategoryName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NotifyLocale`
--

DROP TABLE IF EXISTS `NotifyLocale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NotifyLocale` (
  `recid` bigint(20) NOT NULL,
  `NotifyLocaleID` varchar(72) DEFAULT NULL,
  `NotifyTemplateID` varchar(72) DEFAULT NULL,
  `LanguageCode` varchar(4) DEFAULT NULL,
  `IsDefault` tinyint(1) DEFAULT NULL,
  `Subject` varchar(400) DEFAULT NULL,
  `EmailMessage` text DEFAULT NULL,
  `InboxMessage` text DEFAULT NULL,
  `InboxIcon` varchar(300) DEFAULT NULL,
  `SmsMessage` text DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `NotifyVersionID` varchar(72) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__notifylocaleunique` (`NotifyVersionID`,`LanguageCode`),
  UNIQUE KEY `idx__notifylocaleid` (`NotifyLocaleID`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NotifyTemplate`
--

DROP TABLE IF EXISTS `NotifyTemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NotifyTemplate` (
  `recid` bigint(20) NOT NULL,
  `NotifyTemplateID` varchar(72) DEFAULT NULL,
  `TemplateName` varchar(160) DEFAULT NULL,
  `Description` varchar(400) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `TemplateOwner` varchar(160) DEFAULT NULL,
  `IsInternal` tinyint(1) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__notifytemplateid` (`NotifyTemplateID`),
  UNIQUE KEY `idx__notifytemplate` (`TemplateName`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `NotifyVersion`
--

DROP TABLE IF EXISTS `NotifyVersion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NotifyVersion` (
  `recid` bigint(20) NOT NULL,
  `NotifyVersionID` varchar(72) DEFAULT NULL,
  `NotifyTemplateID` varchar(72) DEFAULT NULL,
  `TemplateVersion` varchar(200) DEFAULT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `TenantID` varchar(340) DEFAULT NULL,
  `Description` varchar(400) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `CreatedBy` varchar(32) DEFAULT NULL,
  `CreatedDateTime` timestamp(3) NULL DEFAULT NULL,
  `CreatedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastUpdateUser` varchar(32) DEFAULT NULL,
  `LastUpdateDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastUpdateDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__notifyversionid` (`NotifyVersionID`),
  UNIQUE KEY `idx__notifyversion` (`NotifyTemplateID`,`TemplateVersion`,`AppURI`,`TenantID`) USING HASH,
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `PermissionType`
--

DROP TABLE IF EXISTS `PermissionType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PermissionType` (
  `recid` bigint(20) NOT NULL,
  `PermissionTypeID` varchar(72) NOT NULL,
  `PermissionType` varchar(32) NOT NULL,
  `StringCode` varchar(80) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__permissiontypeid` (`PermissionTypeID`),
  UNIQUE KEY `idx__permissiontype` (`PermissionType`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDatetime`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ProfileType`
--

DROP TABLE IF EXISTS `ProfileType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProfileType` (
  `recid` bigint(20) NOT NULL,
  `ProfileTypeCode` varchar(30) NOT NULL,
  `SharedSetTypeCode` varchar(20) NOT NULL,
  `ProfileTypeTranslated` varchar(20) DEFAULT NULL,
  `ProfileTypeIsActive` tinyint(1) NOT NULL,
  `ProfileTypeIsDefault` tinyint(1) NOT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`ProfileTypeCode`),
  KEY `idx__viewindex` (`ProfileTypeIsActive`,`ProfileTypeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RelatedEntity`
--

DROP TABLE IF EXISTS `RelatedEntity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RelatedEntity` (
  `recid` bigint(20) NOT NULL,
  `RelatedEntityID` varchar(72) DEFAULT NULL,
  `EntityID` varchar(72) DEFAULT NULL,
  `EntityTableCode` varchar(160) DEFAULT NULL,
  `RelatedEntityCode` varchar(80) DEFAULT NULL,
  `RelatedEntityTableCode` varchar(160) DEFAULT NULL,
  `EntityFields` varchar(256) DEFAULT NULL,
  `EntityRelatedFields` varchar(256) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  KEY `idx__entityid` (`EntityID`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__relatedentityid` (`RelatedEntityID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RelatedField`
--

DROP TABLE IF EXISTS `RelatedField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RelatedField` (
  `recid` bigint(20) NOT NULL,
  `RelatedFieldID` varchar(72) DEFAULT NULL,
  `ViewURI` varchar(340) DEFAULT NULL,
  `ComponentURI` varchar(340) DEFAULT NULL,
  `RelatedComponentURI` varchar(340) DEFAULT NULL,
  `KeyFieldsURI` text DEFAULT NULL,
  `RelatedFieldName` varchar(100) DEFAULT NULL,
  `SerializedFieldName` varchar(100) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__relatedfieldid` (`RelatedFieldID`),
  UNIQUE KEY `idx__relatedfieldmeta` (`ViewURI`,`ComponentURI`,`KeyFieldsURI`,`RelatedFieldName`) USING HASH,
  KEY `idx__relfldmoduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RelatedFieldRel`
--

DROP TABLE IF EXISTS `RelatedFieldRel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RelatedFieldRel` (
  `recid` bigint(20) NOT NULL,
  `RelatedFieldRelID` varchar(72) DEFAULT NULL,
  `RelatedFieldID` varchar(72) DEFAULT NULL,
  `RelationSequence` int(11) DEFAULT NULL,
  `RelationID` varchar(72) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__relatedfieldrelid` (`RelatedFieldRelID`),
  UNIQUE KEY `idx__relatedfieldrelation` (`RelatedFieldID`,`RelationSequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ResourceDependency`
--

DROP TABLE IF EXISTS `ResourceDependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourceDependency` (
  `recid` bigint(20) NOT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `DependencyURI` varchar(340) DEFAULT NULL,
  `Relationship` varchar(32) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `Permissions` varchar(240) DEFAULT NULL,
  `DependencyStringCode` varchar(260) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__resourcedependencyrelationship` (`ResourceURI`,`DependencyURI`,`Relationship`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`),
  KEY `idx__relationship` (`Relationship`,`recid`),
  KEY `idx__resourceuri` (`ResourceURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ResourceIdentity`
--

DROP TABLE IF EXISTS `ResourceIdentity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourceIdentity` (
  `recid` bigint(20) NOT NULL,
  `ResourceIdentityID` varchar(72) DEFAULT NULL,
  `ResourceType` varchar(100) DEFAULT NULL,
  `Identity` varchar(300) DEFAULT NULL,
  `ParentURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `IsInheriting` tinyint(1) DEFAULT NULL,
  `StringCode` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__resourceuri` (`ResourceURI`),
  UNIQUE KEY `idx__resourceidentityid` (`ResourceIdentityID`),
  KEY `idx__parenturi` (`ParentURI`,`recid`),
  KEY `idx__resourcetype` (`ResourceType`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ResourceMapping`
--

DROP TABLE IF EXISTS `ResourceMapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourceMapping` (
  `recid` bigint(20) NOT NULL,
  `QraResourceURI` varchar(340) DEFAULT NULL,
  `EEResourceURI` varchar(340) DEFAULT NULL,
  `Permissions` varchar(240) DEFAULT NULL,
  `MappingType` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__qraresourceeeresourcetype` (`QraResourceURI`,`EEResourceURI`,`MappingType`),
  KEY `idx__eeresourcetype` (`EEResourceURI`,`MappingType`,`recid`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ResourcePermissionType`
--

DROP TABLE IF EXISTS `ResourcePermissionType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourcePermissionType` (
  `recid` bigint(20) NOT NULL,
  `ResourcePermissionTypeID` varchar(72) NOT NULL,
  `ResourceType` varchar(100) DEFAULT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `PermissionType` varchar(32) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDatetime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDatetime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__resourcepermissiontypeid` (`ResourcePermissionTypeID`),
  UNIQUE KEY `idx__restypeuriperm` (`ResourceType`,`ResourceURI`,`PermissionType`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDatetime`,`recid`),
  KEY `idx__permissiontype` (`PermissionType`,`recid`),
  KEY `idx__resourceuri` (`ResourceURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Role`
--

DROP TABLE IF EXISTS `Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Role` (
  `recid` bigint(20) NOT NULL,
  `Role_ID` bigint(20) NOT NULL,
  `BusComponent_ID` bigint(20) DEFAULT NULL,
  `RoleName` varchar(20) NOT NULL,
  `RoleDescription` varchar(24) NOT NULL,
  `RoleIsActive` tinyint(1) NOT NULL,
  `RoleBusComponentConcept` varchar(20) DEFAULT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `CustomShort0` varchar(20) DEFAULT NULL,
  `CustomShort1` varchar(20) DEFAULT NULL,
  `CustomShort2` varchar(20) DEFAULT NULL,
  `CustomShort3` varchar(20) DEFAULT NULL,
  `CustomShort4` varchar(20) DEFAULT NULL,
  `CustomShort5` varchar(20) DEFAULT NULL,
  `CustomShort6` varchar(20) DEFAULT NULL,
  `CustomShort7` varchar(20) DEFAULT NULL,
  `CustomShort8` varchar(20) DEFAULT NULL,
  `CustomShort9` varchar(20) DEFAULT NULL,
  `CustomCombo0` varchar(20) DEFAULT NULL,
  `CustomCombo1` varchar(20) DEFAULT NULL,
  `CustomCombo2` varchar(20) DEFAULT NULL,
  `CustomCombo3` varchar(20) DEFAULT NULL,
  `CustomCombo4` varchar(20) DEFAULT NULL,
  `CustomCombo5` varchar(20) DEFAULT NULL,
  `CustomCombo6` varchar(20) DEFAULT NULL,
  `CustomCombo7` varchar(20) DEFAULT NULL,
  `CustomCombo8` varchar(20) DEFAULT NULL,
  `CustomCombo9` varchar(20) DEFAULT NULL,
  `CustomLong0` varchar(255) DEFAULT NULL,
  `CustomLong1` varchar(255) DEFAULT NULL,
  `CustomNote` text DEFAULT NULL,
  `CustomDate0` date DEFAULT NULL,
  `CustomDate1` date DEFAULT NULL,
  `CustomDate2` date DEFAULT NULL,
  `CustomDate3` date DEFAULT NULL,
  `CustomDate4` date DEFAULT NULL,
  `CustomInteger0` int(11) DEFAULT NULL,
  `CustomInteger1` int(11) DEFAULT NULL,
  `CustomInteger2` int(11) DEFAULT NULL,
  `CustomInteger3` int(11) DEFAULT NULL,
  `CustomInteger4` int(11) DEFAULT NULL,
  `CustomDecimal0` decimal(50,4) DEFAULT NULL,
  `CustomDecimal1` decimal(50,4) DEFAULT NULL,
  `CustomDecimal2` decimal(50,4) DEFAULT NULL,
  `CustomDecimal3` decimal(50,4) DEFAULT NULL,
  `CustomDecimal4` decimal(50,4) DEFAULT NULL,
  `RoleSODException` tinyint(1) NOT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  `RoleModuleURI` varchar(170) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__rolename` (`RoleName`),
  UNIQUE KEY `idx__prim` (`Role_ID`),
  KEY `idx__component` (`BusComponent_ID`,`recid`),
  KEY `idx__sodexcptidx` (`RoleSODException`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RoleResource`
--

DROP TABLE IF EXISTS `RoleResource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RoleResource` (
  `recid` bigint(20) NOT NULL,
  `RoleResource_ID` bigint(20) NOT NULL,
  `Resource_ID` bigint(20) NOT NULL,
  `Role_ID` bigint(20) NOT NULL,
  `RoleResourceIsDefault` tinyint(1) NOT NULL,
  `LastModifiedDate` date DEFAULT NULL,
  `LastModifiedTime` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(20) DEFAULT NULL,
  `QADC01` varchar(40) DEFAULT NULL,
  `QADC02` varchar(510) DEFAULT NULL,
  `QADT01` date DEFAULT NULL,
  `QADD01` decimal(50,10) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`RoleResource_ID`),
  KEY `idx__resource_fk` (`Resource_ID`,`recid`),
  KEY `idx__role_fk` (`Role_ID`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ServerScript`
--

DROP TABLE IF EXISTS `ServerScript`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ServerScript` (
  `recid` bigint(20) NOT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `AppSequence` int(11) DEFAULT NULL,
  `ScriptName` varchar(80) DEFAULT NULL,
  `ScriptSequence` int(11) DEFAULT NULL,
  `JavaScriptCode` mediumtext DEFAULT NULL,
  `TypeScriptCode` mediumtext DEFAULT NULL,
  `TypeDefinitionCode` mediumtext DEFAULT NULL,
  `MappingCode` mediumtext DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `IsEnabled` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`AppURI`,`ScriptName`),
  KEY `idx__enabled` (`IsEnabled`,`recid`),
  KEY `idx__lastmodifieddatetime` (`LastModifiedDateTime`,`recid`),
  KEY `idx__seq` (`AppSequence`,`ScriptSequence`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ServiceMetadata`
--

DROP TABLE IF EXISTS `ServiceMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ServiceMetadata` (
  `recid` bigint(20) NOT NULL,
  `ServiceId` varchar(160) DEFAULT NULL,
  `ServiceURI` varchar(340) DEFAULT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `ServiceResourceURI` varchar(340) DEFAULT NULL,
  `SecureResourceURI` varchar(340) DEFAULT NULL,
  `ServiceVersion` int(11) DEFAULT NULL,
  `ServiceLanguage` varchar(160) DEFAULT NULL,
  `ServiceType` varchar(160) DEFAULT NULL,
  `ServicePath` varchar(340) DEFAULT NULL,
  `ServiceMethod` varchar(160) DEFAULT NULL,
  `ServiceName` varchar(200) DEFAULT NULL,
  `ServiceDescription` varchar(500) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__serviceidprimary` (`ServiceId`),
  KEY `idx__appuriactive` (`AppURI`,`recid`),
  KEY `idx__secureresourceuriactive` (`SecureResourceURI`,`recid`),
  KEY `idx__servicepathactive` (`ServicePath`,`recid`),
  KEY `idx__serviceuriactive` (`ServiceURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ServiceParam`
--

DROP TABLE IF EXISTS `ServiceParam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ServiceParam` (
  `recid` bigint(20) NOT NULL,
  `ServiceId` varchar(160) DEFAULT NULL,
  `ServiceParamId` varchar(160) DEFAULT NULL,
  `ServiceParamIndex` int(11) DEFAULT NULL,
  `ServiceParamMode` varchar(100) DEFAULT NULL,
  `ServiceParamDatatype` varchar(100) DEFAULT NULL,
  `ServiceParamName` varchar(160) DEFAULT NULL,
  `ServiceParamExtent` int(11) DEFAULT NULL,
  `ServiceParamSchema` varchar(340) DEFAULT NULL,
  `JsonName` varchar(160) DEFAULT NULL,
  `ServiceParamDescription` varchar(500) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__serviceparamidprimary` (`ServiceParamId`),
  KEY `idx__paramnameactive` (`ServiceParamName`,`recid`),
  KEY `idx__serviceidparamidactive` (`ServiceId`,`ServiceParamId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ServiceRest`
--

DROP TABLE IF EXISTS `ServiceRest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ServiceRest` (
  `recid` bigint(20) NOT NULL,
  `RestId` varchar(160) DEFAULT NULL,
  `ServiceURI` varchar(340) DEFAULT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `UrlPath` text DEFAULT NULL,
  `UrlMethod` varchar(160) DEFAULT NULL,
  `ServiceVersion` int(11) DEFAULT NULL,
  `ServicePath` varchar(340) DEFAULT NULL,
  `HttpMethod` varchar(40) DEFAULT NULL,
  `RestParamType` varchar(40) DEFAULT NULL,
  `IsEnabled` tinyint(1) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__restidprimary` (`RestId`),
  KEY `idx__appuriactive` (`AppURI`,`recid`),
  KEY `idx__pathversionactive` (`ServicePath`,`ServiceVersion`,`recid`),
  KEY `idx__servicepathactive` (`ServicePath`,`recid`),
  KEY `idx__serviceuriactive` (`ServiceURI`,`recid`),
  KEY `idx__urlmethodactive` (`UrlMethod`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `StoredView`
--

DROP TABLE IF EXISTS `StoredView`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StoredView` (
  `recid` bigint(20) NOT NULL,
  `StoredViewID` varchar(72) DEFAULT NULL,
  `ViewName` varchar(80) DEFAULT NULL,
  `ViewData` mediumtext DEFAULT NULL,
  `Level` varchar(2) DEFAULT NULL,
  `ResourceURI` varchar(340) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `Usrid` varchar(32) DEFAULT NULL,
  `IsQADStandard` tinyint(1) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `IsMobile` tinyint(1) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `IsDefault` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__alt` (`ResourceURI`,`ViewName`,`Level`,`Usrid`),
  UNIQUE KEY `idx__prim` (`StoredViewID`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `StoredViewRoleDomain`
--

DROP TABLE IF EXISTS `StoredViewRoleDomain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StoredViewRoleDomain` (
  `recid` bigint(20) NOT NULL,
  `StoredViewID` varchar(72) DEFAULT NULL,
  `RoleName` varchar(40) DEFAULT NULL,
  `DomainCode` varchar(16) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__prim` (`StoredViewID`,`RoleName`,`DomainCode`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Theme`
--

DROP TABLE IF EXISTS `Theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Theme` (
  `recid` bigint(20) NOT NULL,
  `ThemeID` varchar(72) DEFAULT NULL,
  `Name` varchar(256) DEFAULT NULL,
  `Description` varchar(256) DEFAULT NULL,
  `BrandImage` longblob DEFAULT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__themeid` (`ThemeID`),
  UNIQUE KEY `idx__appuriname` (`AppURI`,`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ThemeImage`
--

DROP TABLE IF EXISTS `ThemeImage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ThemeImage` (
  `recid` bigint(20) NOT NULL,
  `ThemeImageID` varchar(72) DEFAULT NULL,
  `ThemeID` varchar(72) DEFAULT NULL,
  `ImageSource` varchar(256) DEFAULT NULL,
  `Image` longblob DEFAULT NULL,
  `Context` varchar(256) DEFAULT NULL,
  `ImageType` varchar(256) DEFAULT NULL,
  `Position_` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__themeidcontext` (`ThemeID`,`Context`),
  UNIQUE KEY `idx__themeimageid` (`ThemeImageID`),
  KEY `idx__themeidthemeimageid` (`ThemeID`,`ThemeImageID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ThemePalette`
--

DROP TABLE IF EXISTS `ThemePalette`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ThemePalette` (
  `recid` bigint(20) NOT NULL,
  `ThemePaletteID` varchar(72) DEFAULT NULL,
  `ThemeID` varchar(72) DEFAULT NULL,
  `Sequence` varchar(50) DEFAULT NULL,
  `SequenceColor` varchar(14) DEFAULT NULL,
  `Light` varchar(14) DEFAULT NULL,
  `Regular` varchar(14) DEFAULT NULL,
  `Dark` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__themepaletteid` (`ThemePaletteID`),
  UNIQUE KEY `idx__themeidsequence` (`ThemeID`,`Sequence`),
  KEY `idx__themeidthemepaletteid` (`ThemeID`,`ThemePaletteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ThemeProperty`
--

DROP TABLE IF EXISTS `ThemeProperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ThemeProperty` (
  `recid` bigint(20) NOT NULL,
  `ThemePropertyID` varchar(72) DEFAULT NULL,
  `ThemeID` varchar(72) DEFAULT NULL,
  `Property` varchar(256) DEFAULT NULL,
  `PropertyValue` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__themeidproperty` (`ThemeID`,`Property`),
  UNIQUE KEY `idx__themepropertyid` (`ThemePropertyID`),
  KEY `idx__themeidthemepropertyid` (`ThemeID`,`ThemePropertyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TranslatedString`
--

DROP TABLE IF EXISTS `TranslatedString`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TranslatedString` (
  `recid` bigint(20) NOT NULL,
  `StringCode` varchar(260) DEFAULT NULL,
  `LanguageCode` varchar(6) DEFAULT NULL,
  `RegionCode` varchar(6) DEFAULT NULL,
  `StringText` text DEFAULT NULL,
  `Timestamp` varchar(64) DEFAULT NULL,
  `AppURI` varchar(340) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__translatedstring` (`StringCode`,`LanguageCode`,`RegionCode`),
  KEY `idx__appidx` (`AppURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TranslatedStringModule`
--

DROP TABLE IF EXISTS `TranslatedStringModule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TranslatedStringModule` (
  `recid` bigint(20) NOT NULL,
  `StringCode` varchar(260) DEFAULT NULL,
  `LanguageCode` varchar(6) DEFAULT NULL,
  `RegionCode` varchar(6) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__translatedstringmodule` (`StringCode`,`LanguageCode`,`RegionCode`,`ModuleURI`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ViewMetadata`
--

DROP TABLE IF EXISTS `ViewMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ViewMetadata` (
  `recid` bigint(20) NOT NULL,
  `ViewID` varchar(36) DEFAULT NULL,
  `PlatformName` varchar(32) DEFAULT NULL,
  `ModuleName` varchar(32) DEFAULT NULL,
  `ViewName` varchar(80) DEFAULT NULL,
  `ViewMetadata` mediumtext DEFAULT NULL,
  `LastModifiedDateTime` timestamp(3) NULL DEFAULT NULL,
  `LastModifiedDateTime_offset` int(11) DEFAULT NULL,
  `LastModifiedUser` varchar(32) DEFAULT NULL,
  `ViewURI` varchar(340) DEFAULT NULL,
  `ParentURI` varchar(340) DEFAULT NULL,
  `IsEligibleForMenu` tinyint(1) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  KEY `idx__entityuri` (`EntityURI`,`recid`),
  KEY `idx__moduleuri` (`ModuleURI`,`recid`),
  KEY `idx__platform` (`PlatformName`,`ModuleName`,`ViewID`,`recid`),
  KEY `idx__viewuri` (`ViewURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ViewResourceMetadata`
--

DROP TABLE IF EXISTS `ViewResourceMetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ViewResourceMetadata` (
  `recid` bigint(20) NOT NULL,
  `MetaURI` varchar(340) DEFAULT NULL,
  `ViewURI` varchar(340) DEFAULT NULL,
  `PrimarySecureURI` varchar(340) DEFAULT NULL,
  `NameStringCode` varchar(80) DEFAULT NULL,
  `IsEligibleForMenu` tinyint(1) DEFAULT NULL,
  `BrowseURI` varchar(340) DEFAULT NULL,
  `ModuleURI` varchar(340) DEFAULT NULL,
  `IsUseBEBrowse` tinyint(1) DEFAULT NULL,
  `Description` varchar(510) DEFAULT NULL,
  `EntityURI` varchar(340) DEFAULT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__metaidx` (`MetaURI`),
  KEY `idx__browseidx` (`BrowseURI`,`recid`),
  KEY `idx__entityuri` (`EntityURI`,`recid`),
  KEY `idx__moduleidx` (`ModuleURI`,`recid`),
  KEY `idx__namestringcodeidx` (`NameStringCode`,`recid`),
  KEY `idx__primarysecureidx` (`PrimarySecureURI`,`recid`),
  KEY `idx__viewidx` (`ViewURI`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brw_mstr`
--

DROP TABLE IF EXISTS `brw_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brw_mstr` (
  `recid` bigint(20) NOT NULL,
  `brw_name` varchar(30) NOT NULL,
  `brw_desc` varchar(80) DEFAULT NULL,
  `brw_view` varchar(30) NOT NULL,
  `brw_cansee` varchar(80) DEFAULT NULL,
  `brw_filter` text DEFAULT NULL,
  `brw_userid` varchar(80) DEFAULT NULL,
  `brw_mod_date` date DEFAULT NULL,
  `brw_user1` varchar(80) DEFAULT NULL,
  `brw_user2` varchar(80) DEFAULT NULL,
  `brw_sort_col` varchar(30) DEFAULT NULL,
  `brw_col_rtn` varchar(30) DEFAULT NULL,
  `brw_pwr_brw` tinyint(1) DEFAULT NULL,
  `brw_lu_brw` tinyint(1) DEFAULT NULL,
  `brw_locked_col` int(11) NOT NULL,
  `brw_upd_brw` tinyint(1) NOT NULL,
  `brw_include` varchar(30) NOT NULL,
  `brw__qadc01` varchar(80) NOT NULL,
  `brw__qadc02` varchar(80) NOT NULL,
  `oid_brw_mstr` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__brw_mstr` (`brw_name`),
  KEY `idx__brw_desc` (`brw_desc`,`brw_name`),
  KEY `idx__brw_view` (`brw_view`,`brw_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brwf_det`
--

DROP TABLE IF EXISTS `brwf_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brwf_det` (
  `recid` bigint(20) NOT NULL,
  `brw_name` varchar(30) NOT NULL,
  `brwf_seq` int(11) NOT NULL,
  `brwf_field` varchar(30) NOT NULL,
  `brwf_datatype` varchar(30) NOT NULL,
  `brwf_format` varchar(80) NOT NULL,
  `brwf_label` varchar(80) DEFAULT NULL,
  `brwf_col_label` varchar(80) DEFAULT NULL,
  `brwf_expression` varchar(80) DEFAULT NULL,
  `brwf_table` varchar(30) NOT NULL,
  `brwf_select` tinyint(1) NOT NULL,
  `brwf_sort` tinyint(1) NOT NULL,
  `brwf_userid` varchar(80) DEFAULT NULL,
  `brwf_mod_date` date DEFAULT NULL,
  `brwf_user1` varchar(80) DEFAULT NULL,
  `brwf_user2` varchar(80) DEFAULT NULL,
  `brwf__qadc01` varchar(80) DEFAULT NULL,
  `brwf__qadc02` varchar(80) DEFAULT NULL,
  `brwf_enable` tinyint(1) NOT NULL,
  `oid_brwf_det` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__brwf_det` (`brw_name`,`brwf_seq`),
  KEY `idx__brwf_field` (`brwf_field`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brwt_det`
--

DROP TABLE IF EXISTS `brwt_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brwt_det` (
  `recid` bigint(20) NOT NULL,
  `brw_name` varchar(30) NOT NULL,
  `brwt_seq` int(11) NOT NULL,
  `brwt_table` varchar(30) NOT NULL,
  `brwt_join` text DEFAULT NULL,
  `brwt_where` varchar(255) DEFAULT NULL,
  `brwt_userid` varchar(80) DEFAULT NULL,
  `brwt_mod_date` date DEFAULT NULL,
  `brwt_user1` varchar(80) DEFAULT NULL,
  `brwt_user2` varchar(80) DEFAULT NULL,
  `brwt__qadc01` varchar(80) DEFAULT NULL,
  `brwt__qadc02` varchar(80) DEFAULT NULL,
  `oid_brwt_det` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__brwt_det` (`brw_name`,`brwt_seq`),
  KEY `idx__brwt_table` (`brwt_table`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lbl_mstr`
--

DROP TABLE IF EXISTS `lbl_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lbl_mstr` (
  `recid` bigint(20) NOT NULL,
  `lbl_lang` varchar(30) DEFAULT NULL,
  `lbl_term` varchar(80) DEFAULT NULL,
  `lbl_long` varchar(80) DEFAULT NULL,
  `lbl_medium` varchar(80) DEFAULT NULL,
  `lbl_short` varchar(30) DEFAULT NULL,
  `lbl_stacked` varchar(80) DEFAULT NULL,
  `lbl_desc1` varchar(80) DEFAULT NULL,
  `lbl_desc2` varchar(80) DEFAULT NULL,
  `lbl_mod_userid` varchar(80) DEFAULT NULL,
  `lbl_mod_date` date DEFAULT NULL,
  `lbl_user1` varchar(80) DEFAULT NULL,
  `lbl_user2` varchar(80) DEFAULT NULL,
  `lbl__qadc01` varchar(80) DEFAULT NULL,
  `lbl__qadc02` varchar(80) DEFAULT NULL,
  `lbl__qadi01` int(11) DEFAULT NULL,
  `lbl__qadl01` tinyint(1) DEFAULT NULL,
  `lbl__qadt01` date DEFAULT NULL,
  `lbl__qadd01` decimal(50,10) DEFAULT NULL,
  `oid_lbl_mstr` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lbl_term` (`lbl_lang`,`lbl_term`),
  KEY `idx__lbl_long` (`lbl_lang`,`lbl_long`,`recid`),
  KEY `idx__lbl_medium` (`lbl_lang`,`lbl_medium`,`recid`),
  KEY `idx__lbl_short` (`lbl_lang`,`lbl_short`,`recid`),
  KEY `idx__lbl_stacked` (`lbl_lang`,`lbl_stacked`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lbld_det`
--

DROP TABLE IF EXISTS `lbld_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lbld_det` (
  `recid` bigint(20) NOT NULL,
  `lbld_term` varchar(80) DEFAULT NULL,
  `lbld_fieldname` varchar(80) DEFAULT NULL,
  `lbld_execname` varchar(80) DEFAULT NULL,
  `lbld_userid` varchar(80) DEFAULT NULL,
  `lbld_mod_userid` varchar(80) DEFAULT NULL,
  `lbld_mod_date` date DEFAULT NULL,
  `lbld_user1` varchar(80) DEFAULT NULL,
  `lbld_user2` varchar(80) DEFAULT NULL,
  `lbld__qadc01` varchar(80) DEFAULT NULL,
  `lbld__qadc02` varchar(80) DEFAULT NULL,
  `lbld__qadi01` int(11) DEFAULT NULL,
  `lbld__qadl01` tinyint(1) DEFAULT NULL,
  `lbld__qadt01` date DEFAULT NULL,
  `lbld__qadd01` decimal(50,10) DEFAULT NULL,
  `oid_lbld_det` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__lbld_execname` (`lbld_execname`,`lbld_fieldname`),
  KEY `idx__lbld_fieldname` (`lbld_fieldname`,`lbld_execname`),
  KEY `idx__lbld_term` (`lbld_term`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lngd_det`
--

DROP TABLE IF EXISTS `lngd_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lngd_det` (
  `recid` bigint(20) NOT NULL,
  `lngd_dataset` varchar(80) DEFAULT NULL,
  `lngd_key1` varchar(80) DEFAULT NULL,
  `lngd_key2` varchar(80) DEFAULT NULL,
  `lngd_key3` varchar(80) DEFAULT NULL,
  `lngd_key4` varchar(80) DEFAULT NULL,
  `lngd_field` varchar(80) DEFAULT NULL,
  `lngd_lang` varchar(30) DEFAULT NULL,
  `lngd_translation` varchar(30) DEFAULT NULL,
  `lngd_user1` varchar(80) DEFAULT NULL,
  `lngd_user2` varchar(80) DEFAULT NULL,
  `lngd_desc` varchar(80) DEFAULT NULL,
  `lngd_mnemonic` varchar(80) DEFAULT NULL,
  `lngd_translate2` varchar(30) DEFAULT NULL,
  `lngd__qadc01` varchar(80) DEFAULT NULL,
  `oid_lngd_det` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__oid_lngd_det` (`oid_lngd_det`),
  UNIQUE KEY `idx__lngd_det` (`lngd_dataset`,`lngd_key1`,`lngd_key2`,`lngd_key3`,`lngd_key4`,`lngd_field`,`lngd_lang`),
  KEY `idx__lngd_mnemonic` (`lngd_desc`,`lngd_field`,`lngd_lang`,`lngd_mnemonic`,`recid`),
  KEY `idx__lngd_trans` (`lngd_dataset`,`lngd_field`,`lngd_lang`,`lngd_translation`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meta_user`
--

DROP TABLE IF EXISTS `meta_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meta_user` (
  `recid` bigint(20) NOT NULL,
  `_Userid` varchar(32) NOT NULL,
  `_Password` varchar(32) NOT NULL,
  `_User_Name` varchar(80) DEFAULT NULL,
  `_U_misc1_1` int(11) DEFAULT NULL,
  `_U_misc1_2` int(11) DEFAULT NULL,
  `_U_misc1_3` int(11) DEFAULT NULL,
  `_U_misc1_4` int(11) DEFAULT NULL,
  `_U_misc1_5` int(11) DEFAULT NULL,
  `_U_misc1_6` int(11) DEFAULT NULL,
  `_U_misc1_7` int(11) DEFAULT NULL,
  `_U_misc1_8` int(11) DEFAULT NULL,
  `_U_misc2_1` varchar(144) DEFAULT NULL,
  `_U_misc2_2` varchar(144) DEFAULT NULL,
  `_U_misc2_3` varchar(144) DEFAULT NULL,
  `_U_misc2_4` varchar(144) DEFAULT NULL,
  `_U_misc2_5` varchar(144) DEFAULT NULL,
  `_U_misc2_6` varchar(144) DEFAULT NULL,
  `_U_misc2_7` varchar(144) DEFAULT NULL,
  `_U_misc2_8` varchar(144) DEFAULT NULL,
  `_User_Misc` varchar(20) DEFAULT NULL,
  `_User_number` int(11) DEFAULT NULL,
  `_Group_number` int(11) DEFAULT NULL,
  `_Given_name` varchar(25) DEFAULT NULL,
  `_Middle_initial` varchar(1) DEFAULT NULL,
  `_Surname` varchar(25) DEFAULT NULL,
  `_Telephone` varchar(20) DEFAULT NULL,
  `_Email` varchar(50) DEFAULT NULL,
  `_Description` varchar(64) DEFAULT NULL,
  `_Disabled` tinyint(1) DEFAULT NULL,
  `_Create_date` timestamp(3) NULL DEFAULT NULL,
  `_Create_date_offset` int(11) DEFAULT NULL,
  `_Account_expires` timestamp(3) NULL DEFAULT NULL,
  `_Account_expires_offset` int(11) DEFAULT NULL,
  `_Pwd_expires` timestamp(3) NULL DEFAULT NULL,
  `_Pwd_expires_offset` int(11) DEFAULT NULL,
  `_Pwd_duration` int(11) DEFAULT NULL,
  `_Last_login` timestamp(3) NULL DEFAULT NULL,
  `_Last_login_offset` int(11) DEFAULT NULL,
  `_Logins` int(11) DEFAULT NULL,
  `_Max_logins` int(11) DEFAULT NULL,
  `_Max_tries` int(11) DEFAULT NULL,
  `_Login_failures` int(11) DEFAULT NULL,
  `_Spare1` int(11) DEFAULT NULL,
  `_Spare2` int(11) DEFAULT NULL,
  `_Spare3` varchar(1) DEFAULT NULL,
  `_Spare4` varchar(1) DEFAULT NULL,
  `_TenantId` int(11) NOT NULL,
  `_Domain_Name` varchar(64) NOT NULL,
  `_sql_only_user` tinyint(1) NOT NULL,
  PRIMARY KEY (`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mnd_det`
--

DROP TABLE IF EXISTS `mnd_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mnd_det` (
  `recid` bigint(20) NOT NULL,
  `mnd_nbr` varchar(30) NOT NULL,
  `mnd_select` int(11) NOT NULL,
  `mnd_label` varchar(80) NOT NULL,
  `mnd_exec` varchar(30) NOT NULL,
  `mnd_fkey` int(11) DEFAULT NULL,
  `mnd_help` varchar(30) DEFAULT NULL,
  `mnd_canrun` varchar(378) NOT NULL,
  `mnd_name` varchar(80) DEFAULT NULL,
  `mnd_user1` varchar(80) DEFAULT NULL,
  `mnd_user2` varchar(80) DEFAULT NULL,
  `mnd__qadc01` varchar(80) DEFAULT NULL,
  `oid_mnd_det` decimal(50,10) NOT NULL,
  `mnd_uri` varchar(256) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__mnd_nbr` (`mnd_nbr`,`mnd_select`),
  UNIQUE KEY `idx__oid_mnd_det` (`oid_mnd_det`),
  KEY `idx__mnd_exec` (`mnd_exec`,`recid`),
  KEY `idx__mnd_name` (`mnd_name`,`recid`),
  KEY `idx__mnd_uri` (`mnd_uri`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mnt_det`
--

DROP TABLE IF EXISTS `mnt_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mnt_det` (
  `recid` bigint(20) NOT NULL,
  `mnt_nbr` varchar(30) DEFAULT NULL,
  `mnt_select` int(11) DEFAULT NULL,
  `mnt_lang` varchar(30) DEFAULT NULL,
  `mnt_label` varchar(80) DEFAULT NULL,
  `mnt_user1` varchar(80) DEFAULT NULL,
  `mnt_user2` varchar(80) DEFAULT NULL,
  `mnt__qadc01` varchar(80) DEFAULT NULL,
  `oid_mnt_det` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__oid_mnt_det` (`oid_mnt_det`),
  UNIQUE KEY `idx__mnt_nsl` (`mnt_nbr`,`mnt_select`,`mnt_lang`),
  KEY `idx__mnt_lang` (`mnt_lang`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `msg_mstr`
--

DROP TABLE IF EXISTS `msg_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `msg_mstr` (
  `recid` bigint(20) NOT NULL,
  `msg_nbr` int(11) NOT NULL,
  `msg_desc` varchar(80) DEFAULT NULL,
  `msg_lang` varchar(30) DEFAULT NULL,
  `msg_user1` varchar(80) DEFAULT NULL,
  `msg_user2` varchar(80) DEFAULT NULL,
  `msg_type` varchar(80) DEFAULT NULL,
  `msg_explanation_1` text DEFAULT NULL,
  `msg_explanation_2` text DEFAULT NULL,
  `msg_explanation_3` text DEFAULT NULL,
  `msg_explanation_4` text DEFAULT NULL,
  `msg_explanation_5` text DEFAULT NULL,
  `msg_explanation_6` text DEFAULT NULL,
  `msg_explanation_7` text DEFAULT NULL,
  `msg_explanation_8` text DEFAULT NULL,
  `msg_explanation_9` text DEFAULT NULL,
  `msg_explanation_10` text DEFAULT NULL,
  `msg_explanation_11` text DEFAULT NULL,
  `msg__qadc01` varchar(80) DEFAULT NULL,
  `oid_msg_mstr` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__oid_msg_mstr` (`oid_msg_mstr`),
  UNIQUE KEY `idx__msg_ln` (`msg_lang`,`msg_nbr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pin_mstr`
--

DROP TABLE IF EXISTS `pin_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pin_mstr` (
  `recid` bigint(20) NOT NULL,
  `pin_product` varchar(30) NOT NULL,
  `pin_desc` varchar(80) DEFAULT NULL,
  `pin_hwm` int(11) DEFAULT NULL,
  `pin_control1` varchar(30) DEFAULT NULL,
  `pin_control2` varchar(30) DEFAULT NULL,
  `pin_control3` varchar(30) DEFAULT NULL,
  `pin_control4` varchar(30) DEFAULT NULL,
  `pin_control5` varchar(30) DEFAULT NULL,
  `pin_inst_date` date DEFAULT NULL,
  `pin_user1` varchar(80) DEFAULT NULL,
  `pin_user2` varchar(80) DEFAULT NULL,
  `pin__qadc01` varchar(80) DEFAULT NULL,
  `pin__qadi01` int(11) DEFAULT NULL,
  `pin__qadd01` decimal(50,10) DEFAULT NULL,
  `pin__qadl01` tinyint(1) DEFAULT NULL,
  `pin__qadt01` date DEFAULT NULL,
  `pin_control6` varchar(30) NOT NULL,
  `pin_inst_time` int(11) NOT NULL,
  `pin_mod_userid` varchar(80) NOT NULL,
  `pin_mod_date` date DEFAULT NULL,
  `pin_aud_days` int(11) NOT NULL,
  `pin_aud_ddate` date DEFAULT NULL,
  `pin_aud_date` date DEFAULT NULL,
  `pin_aud_user` varchar(30) NOT NULL,
  `pin_aud_pswd` varchar(30) NOT NULL,
  `pin_aud_nbr` int(11) NOT NULL,
  `oid_pin_mstr` decimal(50,10) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__pin_product` (`pin_product`),
  UNIQUE KEY `idx__oid_pin_mstr` (`oid_pin_mstr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `txz_mstr`
--

DROP TABLE IF EXISTS `txz_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `txz_mstr` (
  `recid` bigint(20) NOT NULL,
  `txz_tax_zone` varchar(30) NOT NULL,
  `txz_desc` varchar(80) DEFAULT NULL,
  `txz_ctry_code` varchar(30) NOT NULL,
  `txz_state` varchar(30) NOT NULL,
  `txz_county` varchar(30) NOT NULL,
  `txz_city` varchar(30) NOT NULL,
  `txz_zip` varchar(30) NOT NULL,
  `txz_user1` varchar(80) DEFAULT NULL,
  `txz_user2` varchar(80) DEFAULT NULL,
  `txz__log01` tinyint(1) DEFAULT NULL,
  `txz__qad01` varchar(30) DEFAULT NULL,
  `txz__qad02` varchar(30) DEFAULT NULL,
  `txz__qad03` tinyint(1) DEFAULT NULL,
  `txz__qadc01` varchar(80) NOT NULL,
  `oid_txz_mstr` decimal(50,10) NOT NULL,
  `txz_sums_tax_zone` varchar(30) NOT NULL,
  `txz_reporting` tinyint(1) NOT NULL,
  `txz_sub_total` tinyint(1) NOT NULL,
  PRIMARY KEY (`recid`),
  UNIQUE KEY `idx__txz_ctry_state` (`txz_ctry_code`,`txz_state`,`txz_county`,`txz_city`,`txz_zip`),
  UNIQUE KEY `idx__oid_txz_mstr` (`oid_txz_mstr`),
  UNIQUE KEY `idx__txz_tax_zone` (`txz_tax_zone`),
  KEY `idx__txz_desc` (`txz_desc`,`recid`),
  KEY `idx__txz_sums_tax_zone` (`txz_sums_tax_zone`,`recid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-12 19:05:11
