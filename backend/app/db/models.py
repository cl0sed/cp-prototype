"""
Database Models (SQLAlchemy Table Definitions).

This file defines the structure of your database tables using SQLAlchemy ORM models.
Each class typically represents a table, and its attributes represent columns.

Define table names, columns, data types, relationships (one-to-many, many-to-many),
indexes, and constraints here.

Avoid putting query logic or business logic in model files. Keep them focused
strictly on defining the database schema representation.
"""

# Standard Library Imports
from datetime import datetime
from typing import List, Optional
from uuid import UUID as PyUUID

# Third-Party Imports
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    TIMESTAMP,
    PrimaryKeyConstraint,
    Float,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector  # type: ignore


# --- Base Model ---
class Base(DeclarativeBase):
    pass


# --- Association Tables (Defined early for relationship mapping) ---
class ProjectAudienceAvatar(Base):
    __tablename__ = "project_audience_avatars"
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    audience_avatar_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("audience_avatars.id", ondelete="CASCADE"),
        index=True,
    )

    __table_args__ = (PrimaryKeyConstraint("project_id", "audience_avatar_id"),)

    # Relationships defined in Projects and AudienceAvatars


class ProjectTopicMaterial(Base):
    __tablename__ = "project_topic_materials"
    project_topic_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_topics.id", ondelete="CASCADE"),
        index=True,
    )
    supporting_material_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("supporting_materials.id", ondelete="CASCADE"),
        index=True,
    )

    __table_args__ = (
        PrimaryKeyConstraint("project_topic_id", "supporting_material_id"),
    )

    # Relationships defined in ProjectTopics and SupportingMaterials


# --- Main Models ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    supertokens_user_id: Mapped[Optional[str]] = mapped_column(
        String, unique=True, index=True, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    creator_dna_profiles: Mapped[List["CreatorDnaProfile"]] = relationship(
        "CreatorDnaProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    feedback: Mapped[List["Feedback"]] = relationship(
        "Feedback", back_populates="user", cascade="all, delete-orphan"
    )
    audience_avatars: Mapped[List["AudienceAvatar"]] = relationship(
        "AudienceAvatar",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    supporting_materials: Mapped[List["SupportingMaterial"]] = relationship(
        "SupportingMaterial", back_populates="user", cascade="all, delete-orphan"
    )
    project_settings_templates: Mapped[List["ProjectSettingsTemplate"]] = relationship(
        "ProjectSettingsTemplate", back_populates="user", cascade="all, delete-orphan"
    )
    initiated_background_jobs: Mapped[List["BackgroundJob"]] = relationship(
        "BackgroundJob",
        foreign_keys="BackgroundJob.user_id",
        back_populates="initiating_user",
    )
    retrievable_texts: Mapped[List["RetrievableText"]] = relationship(
        "RetrievableText",
        foreign_keys="RetrievableText.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    dna_detailed_analyses: Mapped[List["DnaDetailedAnalysis"]] = relationship(
        "DnaDetailedAnalysis",
        foreign_keys="DnaDetailedAnalysis.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        foreign_keys="EvaluationResult.evaluating_user_id",
        back_populates="evaluating_user",
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    selected_structure_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("generated_structures.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    educational_framework_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("educational_frameworks.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    active_dna_profile_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("creator_dna_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True)  # "e.g. active, archived"
    creative_brief: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="projects")
    content_sources: Mapped[List["ContentSource"]] = relationship(
        "ContentSource",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    script_sections: Mapped[List["ScriptSection"]] = relationship(
        "ScriptSection",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    research_analyses: Mapped[List["ResearchAnalysis"]] = relationship(
        "ResearchAnalysis", back_populates="project", cascade="all, delete-orphan"
    )
    feedback: Mapped[List["Feedback"]] = relationship(
        "Feedback", back_populates="project", cascade="all, delete-orphan"
    )
    retrievable_texts: Mapped[List["RetrievableText"]] = relationship(
        "RetrievableText",
        foreign_keys="RetrievableText.project_id",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    dna_detailed_analyses: Mapped[List["DnaDetailedAnalysis"]] = relationship(
        "DnaDetailedAnalysis",
        foreign_keys="DnaDetailedAnalysis.project_id",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    background_jobs: Mapped[List["BackgroundJob"]] = relationship(
        "BackgroundJob",
        foreign_keys="BackgroundJob.project_id",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    project_topics: Mapped[List["ProjectTopic"]] = relationship(
        "ProjectTopic", back_populates="project", cascade="all, delete-orphan"
    )
    generated_structures: Mapped[List["GeneratedStructure"]] = relationship(
        "GeneratedStructure",
        foreign_keys="GeneratedStructure.project_id",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    audience_avatars: Mapped[List["AudienceAvatar"]] = relationship(
        "AudienceAvatar",
        secondary="project_audience_avatars",
        back_populates="projects",
    )
    educational_framework: Mapped[Optional["EducationalFramework"]] = relationship(
        "EducationalFramework", back_populates="projects"
    )
    project_settings: Mapped[Optional["ProjectSettings"]] = relationship(
        "ProjectSettings",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    project_idea_validations: Mapped[List["ProjectIdeaValidation"]] = relationship(
        "ProjectIdeaValidation", back_populates="project", cascade="all, delete-orphan"
    )
    active_dna_profile: Mapped[Optional["CreatorDnaProfile"]] = relationship(
        "CreatorDnaProfile", back_populates="active_projects"
    )
    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        foreign_keys="EvaluationResult.project_id",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    selected_structure: Mapped[Optional["GeneratedStructure"]] = relationship(
        "GeneratedStructure",
        foreign_keys=[selected_structure_id],
        back_populates="projects_using_structure",
    )

    evaluation_results_link: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(Project.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'PROJECTS')",
        overlaps="evaluation_results,project",  # Specify overlaps to avoid warnings
        # Consider adding viewonly=True if this is read-only
        # viewonly=True,
    )


class ProjectSettingsTemplate(Base):
    __tablename__ = "project_settings_templates"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    template_name: Mapped[str] = mapped_column(String, nullable=False)
    settings_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    __table_args__ = (
        UniqueConstraint("user_id", "template_name", name="uq_user_template_name"),
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="project_settings_templates"
    )
    project_settings: Mapped[List["ProjectSettings"]] = relationship(
        "ProjectSettings", back_populates="template"
    )


class ProjectSettings(Base):
    __tablename__ = "project_settings"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    template_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_settings_templates.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    setting_overrides: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="project_settings"
    )
    template: Mapped[Optional["ProjectSettingsTemplate"]] = relationship(
        "ProjectSettingsTemplate", back_populates="project_settings"
    )


class AudienceAvatar(Base):
    __tablename__ = "audience_avatars"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audience_avatars")
    projects: Mapped[List["Project"]] = relationship(
        "Project",
        secondary="project_audience_avatars",
        back_populates="audience_avatars",
    )

    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(AudienceAvatar.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'AUDIENCE_AVATARS')",
        cascade="all, delete-orphan",
        # Ensure EvaluationResult has a back_populates if needed
        # back_populates="audience_avatar", # Example
    )


class SupportingMaterial(Base):
    __tablename__ = "supporting_materials"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    material_type: Mapped[str] = mapped_column(String, nullable=False)
    uri: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    material_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="supporting_materials")
    project_topics: Mapped[List["ProjectTopic"]] = relationship(
        "ProjectTopic",
        secondary="project_topic_materials",
        back_populates="supporting_materials",
    )

    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(SupportingMaterial.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'SUPPORTING_MATERIALS')",
        cascade="all, delete-orphan",
        # Ensure EvaluationResult has a back_populates if needed
        # back_populates="supporting_material", # Example
    )


class ProjectTopic(Base):
    __tablename__ = "project_topics"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic_title: Mapped[str] = mapped_column(Text, nullable=False)
    selection_status: Mapped[str] = mapped_column(
        String, index=True
    )  # "e.g. suggested, selected, rejected"
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    parent_topic_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_topics.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="project_topics"
    )
    supporting_materials: Mapped[List["SupportingMaterial"]] = relationship(
        "SupportingMaterial",
        secondary="project_topic_materials",
        back_populates="project_topics",
    )
    parent_topic: Mapped[Optional["ProjectTopic"]] = relationship(
        "ProjectTopic", remote_side=[id], back_populates="child_topics"
    )
    child_topics: Mapped[List["ProjectTopic"]] = relationship(
        "ProjectTopic", back_populates="parent_topic", cascade="all, delete-orphan"
    )

    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(ProjectTopic.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'PROJECT_TOPICS')",
        cascade="all, delete-orphan",
        # Ensure EvaluationResult has a back_populates if needed
        # back_populates="project_topic", # Example
    )


class GeneratedStructure(Base):
    __tablename__ = "generated_structures"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    structure_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", foreign_keys=[project_id], back_populates="generated_structures"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_generated_structures"
    )
    script_sections: Mapped[List["ScriptSection"]] = relationship(
        "ScriptSection", back_populates="generated_structure"
    )
    projects_using_structure: Mapped[List["Project"]] = relationship(
        "Project",
        foreign_keys="Project.selected_structure_id",
        back_populates="selected_structure",
    )

    # Dynamically added relationship from end of file
    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(GeneratedStructure.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'GENERATED_STRUCTURES')",
        cascade="all, delete-orphan",
        # Ensure EvaluationResult has a back_populates if needed
        # back_populates="generated_structure", # Example
    )


class EducationalFramework(Base):
    __tablename__ = "educational_frameworks"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    structure_template: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="educational_framework"
    )


class RetrievableText(Base):
    __tablename__ = "retrievable_text"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    content_source_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("content_sources.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    script_section_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("script_sections.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    basic_metadata: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )  # "Incl. origin_type='story'/'transcript'/etc"
    embedding: Mapped[Vector] = mapped_column(
        Vector(1536), nullable=False
    )  # HNSW Index created separately
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    content_source: Mapped[Optional["ContentSource"]] = relationship(
        "ContentSource", back_populates="retrievable_texts"
    )
    script_section: Mapped[Optional["ScriptSection"]] = relationship(
        "ScriptSection", back_populates="retrievable_texts"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_retrievable_texts"
    )
    project: Mapped["Project"] = relationship(
        "Project", foreign_keys=[project_id], back_populates="retrievable_texts"
    )
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="retrievable_texts"
    )

    # HNSW Index configuration parameters
    # m: max number of connections per node (higher = better recall but more memory)
    # ef_construction: size of dynamic candidate list during index building (higher = better recall but slower build)
    __table_args__ = (
        Index(
            "ix_retrievable_text_embedding",
            embedding,
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
        ),
    )


class DnaDetailedAnalysis(Base):
    __tablename__ = "dna_detailed_analyses"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    content_source_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("content_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pacing_stats: Mapped[dict] = mapped_column(JSONB, nullable=False)
    keyword_analysis: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    content_source: Mapped["ContentSource"] = relationship(
        "ContentSource", back_populates="dna_detailed_analyses"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_dna_analyses"
    )
    project: Mapped["Project"] = relationship(
        "Project", foreign_keys=[project_id], back_populates="dna_detailed_analyses"
    )
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="dna_detailed_analyses"
    )


class ContentSource(Base):
    __tablename__ = "content_sources"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    uri: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Assuming URI is mandatory based on ERD
    raw_transcript: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # Assuming mandatory
    processing_status: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="content_sources"
    )
    retrievable_texts: Mapped[List["RetrievableText"]] = relationship(
        "RetrievableText", back_populates="content_source", cascade="all, delete-orphan"
    )
    dna_detailed_analyses: Mapped[List["DnaDetailedAnalysis"]] = relationship(
        "DnaDetailedAnalysis",
        back_populates="content_source",
        cascade="all, delete-orphan",
    )


class ScriptSection(Base):
    __tablename__ = "script_sections"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    generated_structure_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("generated_structures.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    section_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    parent_section_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("script_sections.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text)  # Current version
    previous_content: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Previous version
    generation_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    hook_options: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="script_sections"
    )
    retrievable_texts: Mapped[List["RetrievableText"]] = relationship(
        "RetrievableText", back_populates="script_section", cascade="all, delete-orphan"
    )
    parent_section: Mapped[Optional["ScriptSection"]] = relationship(
        "ScriptSection", remote_side=[id], back_populates="child_sections"
    )
    child_sections: Mapped[List["ScriptSection"]] = relationship(
        "ScriptSection", back_populates="parent_section", cascade="all, delete-orphan"
    )
    safety_analyses: Mapped[List["SafetyAnalysis"]] = relationship(
        "SafetyAnalysis", back_populates="script_section", cascade="all, delete-orphan"
    )
    generated_structure: Mapped[Optional["GeneratedStructure"]] = relationship(
        "GeneratedStructure", back_populates="script_sections"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_script_sections"
    )
    evaluation_results: Mapped[List["EvaluationResult"]] = relationship(
        "EvaluationResult",
        primaryjoin="and_(ScriptSection.id == foreign(EvaluationResult.target_entity_id), foreign(EvaluationResult.target_entity_type) == 'SCRIPT_SECTIONS')",
        cascade="all, delete-orphan",
        # Ensure EvaluationResult has a back_populates if needed
        # back_populates="script_section", # Example
    )


class ResearchAnalysis(Base):
    __tablename__ = "research_analyses"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    key_findings: Mapped[dict] = mapped_column(JSONB)
    entity_relations: Mapped[dict] = mapped_column(JSONB)
    source_evaluations: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="research_analyses"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_research_analyses"
    )


class SafetyAnalysis(Base):
    __tablename__ = "safety_analyses"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    script_section_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("script_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String, index=True)
    details: Mapped[dict] = mapped_column(JSONB)
    review_timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )  # Assuming mandatory

    # Relationships
    script_section: Mapped["ScriptSection"] = relationship(
        "ScriptSection", back_populates="safety_analyses"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_safety_analyses"
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_entity_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    target_entity_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )  # Polymorphic, no direct FK constraint
    feedback_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="feedback")
    user: Mapped["User"] = relationship("User", back_populates="feedback")


class CreatorDnaProfile(Base):
    __tablename__ = "creator_dna_profiles"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    profile_name: Mapped[str] = mapped_column(String, nullable=False)
    style_notes: Mapped[dict] = mapped_column(JSONB)
    fine_tuning_controls: Mapped[dict] = mapped_column(JSONB)
    source_content_ids: Mapped[Optional[List[PyUUID]]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=True, index=True
    )  # Array of UUIDs, potentially referencing CONTENT_SOURCES? Schema unclear here.
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="creator_dna_profiles")
    active_projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="active_dna_profile"
    )


class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    job_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    task_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    project_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String, nullable=False, index=True)
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, index=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, index=True
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship(
        "Project", foreign_keys=[project_id], back_populates="background_jobs"
    )
    initiating_user: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[user_id], back_populates="initiated_background_jobs"
    )
    initiated_generated_structures: Mapped[List["GeneratedStructure"]] = relationship(
        "GeneratedStructure", back_populates="initiating_job"
    )
    initiated_dna_analyses: Mapped[List["DnaDetailedAnalysis"]] = relationship(
        "DnaDetailedAnalysis", back_populates="initiating_job"
    )
    initiated_research_analyses: Mapped[List["ResearchAnalysis"]] = relationship(
        "ResearchAnalysis", back_populates="initiating_job"
    )
    initiated_safety_analyses: Mapped[List["SafetyAnalysis"]] = relationship(
        "SafetyAnalysis", back_populates="initiating_job"
    )
    initiated_retrievable_texts: Mapped[List["RetrievableText"]] = relationship(
        "RetrievableText", back_populates="initiating_job"
    )
    initiated_script_sections: Mapped[List["ScriptSection"]] = relationship(
        "ScriptSection", back_populates="initiating_job"
    )
    initiated_project_idea_validations: Mapped[List["ProjectIdeaValidation"]] = (
        relationship("ProjectIdeaValidation", back_populates="initiating_job")
    )


class ProjectIdeaValidation(Base):
    __tablename__ = "project_idea_validations"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    initiating_job_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("background_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    validation_results: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="project_idea_validations"
    )
    initiating_job: Mapped[Optional["BackgroundJob"]] = relationship(
        "BackgroundJob", back_populates="initiated_project_idea_validations"
    )


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    evaluating_user_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_entity_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    target_entity_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )  # Polymorphic
    evaluator_type: Mapped[str] = mapped_column(String, nullable=False)  # "AI or USER"
    metric_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", foreign_keys=[project_id], back_populates="evaluation_results"
    )
    evaluating_user: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[evaluating_user_id], back_populates="evaluation_results"
    )

    # Define back-populates relationships for target entities dynamically if needed,
    # or handle polymorphic loading separately using target_entity_type/id.
    # For now, adding basic lists to the target models.


# NOTE: The following relationships were moved into their respective classes above.
# This section is now empty.

# To generate initial migration: alembic revision --autogenerate -m "Add initial database models"
