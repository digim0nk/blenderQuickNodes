# License-Identifier: GPL-3.0-or-later

# Quick Nodes
# Copyright (C) 2025 Lloyd DeAlmeida

bl_info = {
    "name": "Quick Nodes",
    "author": "Lloyd DeAlmeida",
    "version": (1, 0, 0,),
    "blender": (5, 0, 0),
    "location": "Node Editor > Sidebar > Quick Nodes",
    "description": "Quickly add Nodes without using the Keyboard and the Add Menu. Search and Favorites available to speed up workflow.",
    "website_url": "https://github.com/digim0nk/blenderQuickNodes",
    "maintained": "Community",
    "category": "Node",
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty

# Node definitions organized by categories
NODE_CATEGORIES = {
    "INPUT": {
        "Constant": [
            ("ShaderNodeValue", "Value"),
            ("FunctionNodeInputInt", "Integer"),
            ("FunctionNodeInputVector", "Vector"),
            ("FunctionNodeInputBool", "Boolean"),
            ("GeometryNodeInputObject", "Object"),
            ("GeometryNodeInputCollection", "Collection"),
            ("FunctionNodeInputColor", "Color"),
            ("GeometryNodeInputImage", "Image"),
            ("GeometryNodeInputMaterial", "Material"),
            ("FunctionNodeInputRotation", "Rotation"),
            ("FunctionNodeInputString", "String"),
        ],
        "Gizmo": [
            ("GeometryNodeGizmoDial", "Dial Gizmo"),
            ("GeometryNodeGizmoLinear", "Linear Gizmo"),
            ("GeometryNodeGizmoTransform", "Transform Gizmo"),
        ],
        "Group": [
            ("NodeGroupInput", "Group Input"),
        ],
        "Import": [
            ("GeometryNodeImportCSV", "CSV"),
            ("GeometryNodeImportOBJ", "Wavefront"),
            ("GeometryNodeImportPLY", "Stanford"),
            ("GeometryNodeImportSTL", "STL"),
            ("GeometryNodeImportText", "Text"),
            ("GeometryNodeImportVDB", "OpenVDB"),
        ],
        "Scene": [
            ("GeometryNodeObjectInfo", "Object Info"),
            ("GeometryNodeCollectionInfo", "Collection Info"),
            ("GeometryNodeInputSceneTime", "Scene Time"),
            ("GeometryNodeImageInfo", "Image Info"),
            ("GeometryNodeCameraInfo", "Camera Info"),
            ("GeometryNodeInputActiveCamera", "Active Camera"),
            ("GeometryNodeIsViewport", "Is Viewport"),
            ("GeometryNodeSelfObject", "Self Object"),
        ],
    },
    "OUTPUT": [
        ("NodeGroupOutput", "Group Output"),
        ("GeometryNodeViewer", "Viewer"),
        ("GeometryNodeWarning", "Warning"),
    ],
    "ATTRIBUTE": [
        ("GeometryNodeCaptureAttribute", "Capture Attribute"),
        ("GeometryNodeStoreNamedAttribute", "Store Named Attribute"),
        ("GeometryNodeAttributeStatistic", "Attribute Statistic"),
        ("GeometryNodeAttributeDomainSize", "Domain Size"),
        ("GeometryNodeBlurAttribute", "Blur Attribute"),
        ("GeometryNodeRemoveAttribute", "Remove Named Attribute"),
    ],
    "GEOMETRY": {
        "Main Nodes": [
            ("GeometryNodeJoinGeometry", "Join Geometry"),
            ("GeometryNodeGeometryToInstance", "Geometry to Instance"),
            ("GeometryNodeToolSelection3D", "Geometry Input"),
        ],
        "Read": [
            ("GeometryNodeInputPosition", "Position"),
            ("GeometryNodeInputNamedAttribute", "Named Attribute"),
            ("GeometryNodeInputIndex", "Index"),
            ("GeometryNodeInputID", "ID"),
            ("GeometryNodeInputNormal", "Normal"),
            ("GeometryNodeInputRadius", "Radius"),
        ],
        "Sample": [
            ("GeometryNodeProximity", "Geometry Proximity"),
            ("GeometryNodeRaycast", "Raycast"),
            ("GeometryNodeSampleNearest", "Sample Nearest"),
            ("GeometryNodeSampleIndex", "Sample Index"),
            ("GeometryNodeIndexOfNearest", "Index of Nearest"),
        ],
        "Write": [
            ("GeometryNodeSetPosition", "Set Position"),
            ("GeometryNodeSetGeometryName", "Set Geometry Name"),
            ("GeometryNodeSetID", "Set ID"),
        ],
        "Material": [
            ("GeometryNodeSetMaterial", "Set Material"),
            ("GeometryNodeReplaceMaterial", "Replace Material"),
            ("GeometryNodeInputMaterialIndex", "Material Index"),
            ("GeometryNodeMaterialSelection", "Material Selection"),
            ("GeometryNodeSetMaterialIndex", "Set Material Index"),
        ],
        "Operations": [
            ("GeometryNodeDeleteGeometry", "Delete Geometry"),
            ("GeometryNodeMergeByDistance", "Merge by Distance"),
            ("GeometryNodeTransform", "Transform Geometry"),
            ("GeometryNodeSplitToInstances", "Split to Instances"),
            ("GeometryNodeBoundBox", "Bounding Box"),
            ("GeometryNodeConvexHull", "Convex Hull"),
            ("GeometryNodeDisplace", "Displace Geometry"),
            ("GeometryNodeLaplacianSmooth", "Smooth Geometry"),
            ("GeometryNodeDuplicateElements", "Duplicate Elements"),
            ("GeometryNodeSortElements", "Sort Elements"),
            ("GeometryNodeSeparateComponents", "Separate Components"),
            ("GeometryNodeSeparateGeometry", "Separate Geometry"),
            ("GeometryNodeBake", "Bake"),
        ],
        "Selection": [
            ("GeometryNodeToolSelection", "Box Selection"),
            ("GeometryNodeNormalSelection", "Normal Selection"),
            ("GeometryNodeToolSelection", "Sphere Selection"),
        ],
    },
    "CURVE": {
        "Read": [
            ("GeometryNodeSplineParameter", "Spline Parameter"),
            ("GeometryNodeSplineLength", "Spline Length"),
            ("GeometryNodeInputCurveTilt", "Curve Tilt"),
            ("GeometryNodeInputTangent", "Curve Tangent"),
            ("GeometryNodeCurveEndpointSelection", "Endpoint Selection"),
            ("GeometryNodeInputCurveHandlePositions", "Curve Handle Positions"),
            ("GeometryNodeCurveHandleTypeSelection", "Handle Type Selection"),
            ("GeometryNodeInputSplineCyclic", "Is Spline Cyclic"),
            ("GeometryNodeInputSplineResolution", "Spline Resolution"),
            ("GeometryNodeCurveLength", "Curve Length"),
        ],
        "Sample": [
            ("GeometryNodeSampleCurve", "Sample Curve"),
        ],
        "Write": [
            ("GeometryNodeSetCurveRadius", "Set Curve Radius"),
            ("GeometryNodeSetCurveTilt", "Set Curve Tilt"),
            ("GeometryNodeSetCurveNormal", "Set Curve Normal"),
            ("GeometryNodeSetCurveHandlePositions", "Set Handle Positions"),
            ("GeometryNodeCurveSetHandles", "Set Handle Type"),
            ("GeometryNodeSetSplineCyclic", "Set Spline Cyclic"),
            ("GeometryNodeSetSplineResolution", "Set Spline Resolution"),
            ("GeometryNodeCurveSplineType", "Set Spline Type"),
        ],
        "Operations": [
            ("GeometryNodeCurveToMesh", "Curve to Mesh"),
            ("GeometryNodeCurveToPoints", "Curve to Points"),
            ("GeometryNodeResampleCurve", "Resample Curve"),
            ("GeometryNodeTrimCurve", "Trim Curve"),
            ("GeometryNodeReverseCurve", "Reverse Curve"),
            ("GeometryNodeSubdivideCurve", "Subdivide Curve"),
            ("GeometryNodeDeformCurvesOnSurface", "Deform Curves on Surface"),
            ("GeometryNodeFillCurve", "Fill Curve"),
            ("GeometryNodeFilletCurve", "Fillet Curve"),
            ("GeometryNodeInterpolateCurves", "Interpolate Curves"),
            ("GeometryNodeCurvesToGreasePencil", "Curves to Grease Pencil"),
        ],
        "Primitives": [
            ("GeometryNodeCurveArc", "Arc"),
            ("GeometryNodeCurvePrimitiveBezierSegment", "Bézier Segment"),
            ("GeometryNodeCurvePrimitiveCircle", "Curve Circle"),
            ("GeometryNodeCurvePrimitiveLine", "Curve Line"),
            ("GeometryNodeCurveSpiral", "Spiral"),
            ("GeometryNodeCurveQuadraticBezier", "Quadratic Bézier"),
            ("GeometryNodeCurvePrimitiveQuadrilateral", "Quadrilateral"),
            ("GeometryNodeCurveStar", "Star"),
        ],
        "Topology": [
            ("GeometryNodeCurveOfPoint", "Curve of Point"),
            ("GeometryNodeOffsetPointInCurve", "Offset Point in Curve"),
            ("GeometryNodePointsOfCurve", "Points of Curve"),
        ],
    },
    "INSTANCES": [
        ("GeometryNodeInstanceOnPoints", "Instance on Points"),
        ("GeometryNodeInstancesToPoints", "Instances to Points"),
        ("GeometryNodeRealizeInstances", "Realize Instances"),
        ("GeometryNodeRotateInstances", "Rotate Instances"),
        ("GeometryNodeScaleInstances", "Scale Instances"),
        ("GeometryNodeTranslateInstances", "Translate Instances"),
        ("GeometryNodeSetInstanceTransform", "Set Instance Transform"),
        ("GeometryNodeInputInstanceBounds", "Instance Bounds"),
        ("GeometryNodeInstanceTransform", "Instance Transform"),
        ("GeometryNodeInputInstanceRotation", "Instance Rotation"),
        ("GeometryNodeInputInstanceScale", "Instance Scale"),
        ("GeometryNodeInstanceOnElements", "Instance on Elements"),
        ("GeometryNodeRandomizeInstanceTransforms", "Randomize Transforms"),
    ],
    "MESH": {
        "Read": [
            ("GeometryNodeInputMeshEdgeAngle", "Edge Angle"),
            ("GeometryNodeInputMeshEdgeNeighbors", "Edge Neighbors"),
            ("GeometryNodeInputMeshEdgeVertices", "Edge Vertices"),
            ("GeometryNodeEdgesToFaceGroups", "Edges to Face Groups"),
            ("GeometryNodeInputMeshFaceArea", "Face Area"),
            ("GeometryNodeMeshFaceSetBoundaries", "Face Group Boundaries"),
            ("GeometryNodeInputMeshFaceNeighbors", "Face Neighbors"),
            ("GeometryNodeInputMeshFaceIsPlanar", "Is Face Planar"),
            ("GeometryNodeInputShadeSmooth", "Is Face Smooth"),
            ("GeometryNodeInputEdgeSmooth", "Is Edge Smooth"),
            ("GeometryNodeInputMeshIsland", "Mesh Island"),
            ("GeometryNodeInputShortestEdgePaths", "Shortest Edge Paths"),
            ("GeometryNodeInputMeshVertexNeighbors", "Vertex Neighbors"),
            ("GeometryNodeInputEdgeLength", "Edge Length"),
            ("GeometryNodeInputMeshFaceAngle", "Face Corner Angle"),
            ("GeometryNodeInputEdgeIsBoundary", "Is Edge Boundary"),
            ("GeometryNodeInputEdgeIsLoose", "Is Edge Loose"),
            ("GeometryNodeInputEdgeIsManifold", "Is Edge Manifold"),
            ("GeometryNodeInputUVSplit", "Is UV Split"),
        ],
        "Sample": [
            ("GeometryNodeSampleNearestSurface", "Sample Nearest Surface"),
            ("GeometryNodeSampleUVSurface", "Sample UV Surface"),
        ],
        "Write": [
            ("GeometryNodeSetShadeSmooth", "Set Shade Smooth"),
            ("GeometryNodeSetMeshNormal", "Set Mesh Normal"),
        ],
        "Operations": [
            ("GeometryNodeExtrudeMesh", "Extrude Mesh"),
            ("GeometryNodeScaleElements", "Scale Elements"),
            ("GeometryNodeSubdivisionSurface", "Subdivision Surface"),
            ("GeometryNodeSubdivideMesh", "Subdivide Mesh"),
            ("GeometryNodeMeshBoolean", "Mesh Boolean"),
            ("GeometryNodeDualMesh", "Dual Mesh"),
            ("GeometryNodeMeshToPoints", "Mesh to Points"),
            ("GeometryNodeMeshToVolume", "Mesh to Volume"),
            ("GeometryNodeMeshToCurve", "Mesh to Curve"),
            ("GeometryNodeEdgePathsToCurves", "Edge Paths to Curves"),
            ("GeometryNodeEdgePathsToSelection", "Edge Paths to Selection"),
            ("GeometryNodeFlipFaces", "Flip Faces"),
            ("GeometryNodeSplitEdges", "Split Edges"),
            ("GeometryNodeTriangulate", "Triangulate"),
        ],
        "Primitives": [
            ("GeometryNodeMeshCone", "Cone"),
            ("GeometryNodeMeshCube", "Cube"),
            ("GeometryNodeMeshCylinder", "Cylinder"),
            ("GeometryNodeMeshGrid", "Grid"),
            ("GeometryNodeMeshIcoSphere", "Ico Sphere"),
            ("GeometryNodeMeshCircle", "Mesh Circle"),
            ("GeometryNodeMeshLine", "Mesh Line"),
            ("GeometryNodeMeshUVSphere", "UV Sphere"),
        ],
        "Topology": [
            ("GeometryNodeCornersOfEdge", "Corners of Edge"),
            ("GeometryNodeCornersOfFace", "Corners of Face"),
            ("GeometryNodeCornersOfVertex", "Corners of Vertex"),
            ("GeometryNodeEdgesOfCorner", "Edges of Corner"),
            ("GeometryNodeEdgesOfVertex", "Edges of Vertex"),
            ("GeometryNodeFaceOfCorner", "Face of Corner"),
            ("GeometryNodeOffsetCornerInFace", "Offset Corner in Face"),
            ("GeometryNodeVertexOfCorner", "Vertex of Corner"),
        ],
        "UV": [
            ("GeometryNodeUVPackIslands", "Pack UV Islands"),
            ("GeometryNodeUVTangent", "UV Tangent"),
            ("GeometryNodeUVUnwrap", "UV Unwrap"),
        ],
    },
    "POINT": [
        ("GeometryNodeDistributePointsOnFaces", "Distribute Points on Faces"),
        ("GeometryNodeDistributePointsInVolume", "Distribute Points in Volume"),
        ("GeometryNodePoints", "Points"),
        ("GeometryNodeSetPointRadius", "Set Point Radius"),
        ("GeometryNodeDistributePointsInGrid", "Distribute Points in Grid"),
        ("GeometryNodePointsToCurves", "Points to Curves"),
        ("GeometryNodePointsToSDFGrid", "Points to SDF Grid"),
        ("GeometryNodePointsToVertices", "Points to Vertices"),
        ("GeometryNodePointsToVolume", "Points to Volume"),
        
    ],
    "VOLUME": {
        "Read": [
            ("GeometryNodeGetNamedGrid", "Get Named Grid"),
            ("GeometryNodeGridInfo", "Grid Info"),
            ("GeometryNodeInputVoxelIndex", "Voxel Index"),
        ],
        "Sample": [
            ("GeometryNodeSampleGrid", "Sample Grid"),
            ("GeometryNodeSampleGridIndex", "Sample Grid Index"),
            ("GeometryNodeGridCurl", "Advect Grid"),
            ("GeometryNodeGridCurl", "Grid Curl"),
            ("GeometryNodeGridDivergence", "Grid Divergence"),
            ("GeometryNodeGridGradient", "Grid Gradient"),
            ("GeometryNodeGridLaplacian", "Grid Laplacian"),
        ],
        "Write": [
            ("GeometryNodeStoreNamedGrid", "Store Named Grid"),
            ("GeometryNodeSetGridBackground", "Set Grid Background"),
            ("GeometryNodeSetGridTransform", "Set Grid Transform"),
        ],
        "Operations": [
            ("GeometryNodeVolumeToMesh", "Volume to Mesh"),
            ("GeometryNodeGridToMesh", "Grid to Mesh"),
            ("GeometryNodeSDFGridBoolean", "SDF Grid Boolean"),
            ("GeometryNodeSDFGridFillet", "SDF Grid Fillet"),
            ("GeometryNodeSDFGridLaplacian", "SDF Grid Laplacian"),
            ("GeometryNodeSDFGridMean", "SDF Grid Mean"),
            ("GeometryNodeSDFGridMeanCurvature", "SDF Grid Mean Curvature"),
            ("GeometryNodeSDFGridMedian", "SDF Grid Median"),
            ("GeometryNodeSDFGridOffset", "SDF Grid Offset"),
            ("GeometryNodeFieldToGrid", "Field to Grid"),
            ("GeometryNodeGridPrune", "Prune Grid"),
            ("GeometryNodeGridVoxelize", "Voxelize Grid"),
        ],
        "Primitives": [
            ("GeometryNodeVolumeCube", "Volume Cube"),
        ],
    },
    "SIMULATION": [
        ("QUICKNODES_OT_add_simulation_zone", "Simulation Zone"),
    ],
    "COLOR": [
        ("ShaderNodeValToRGB", "Color Ramp"),
        ("ShaderNodeRGBCurve", "RGB Curves"),
        ("ShaderNodeBlackbody", "Blackbody"),
        ("ShaderNodeGamma", "Gamma"),
        ("FunctionNodeCombineColor", "Combine Color"),
        ("FunctionNodeSeparateColor", "Separate Color"),
        ("ShaderNodeMix", "Mix Color"),
    ],
    "TEXTURE": [
        ("ShaderNodeTexNoise", "Noise Texture"),
        ("ShaderNodeTexVoronoi", "Voronoi Texture"),
        ("ShaderNodeTexGabor", "Gabor Texture"),
        ("ShaderNodeTexMagic", "Magic Texture"),
        ("ShaderNodeTexWave", "Wave Texture"),
        ("ShaderNodeTexBrick", "Brick Texture"),
        ("ShaderNodeTexChecker", "Checker Texture"),
        ("ShaderNodeTexGradient", "Gradient Texture"),
        ("GeometryNodeImageTexture", "Image Texture"),
        ("ShaderNodeTexWhiteNoise", "White Noise Texture"),
    ],
    "UTILITIES": {
        "Main Nodes": [
            ("FunctionNodeRandomValue", "Random Value"),
            ("QUICKNODES_OT_add_repeat_zone", "Repeat"),
            ("QUICKNODES_OT_add_foreach_element_zone", "For Each Element"),
            ("FunctionNodeRandomRotation", "Random Rotation"),
            ("GeometryNodeIndexSwitch", "Index Switch"),
            ("GeometryNodeMenuSwitch", "Menu Switch"),
            ("GeometryNodeSwitch", "Switch"),
        ],
        "Math": [
            ("ShaderNodeMath", "Math"),
            ("ShaderNodeFloatCurve", "Float Curve"),
            ("ShaderNodeMapRange", "Map Range"),
            ("FunctionNodeCompare", "Compare"),
            ("FunctionNodeBooleanMath", "Boolean Math"),
            ("FunctionNodeIntegerMath", "Integer Math"),
            ("FunctionNodeBitMath", "Bit Math"),
            ("ShaderNodeClamp", "Clamp"),
            ("FunctionNodeFloatToInt", "Float to Integer"),
            ("FunctionNodeHashValue", "Hash Value"),
            ("ShaderNodeMix", "Mix"),
        ],
        "Text": [
            ("FunctionNodeFormatString", "Format String"),
            ("GeometryNodeStringJoin", "Join Strings"),
            ("FunctionNodeMatchString", "Match String"),
            ("FunctionNodeReplaceString", "Replace String"),
            ("FunctionNodeSliceString", "Slice String"),
            ("FunctionNodeFindInString", "Find in String"),
            ("FunctionNodeStringLength", "String Length"),
            ("GeometryNodeStringToCurves", "String to Curves"),
            ("FunctionNodeStringToValue", "String to Value"),
            ("FunctionNodeValueToString", "Value to String"),
            ("FunctionNodeInputSpecialCharacters", "Special Characters"),
        ],
        "Vector": [
            ("ShaderNodeVectorMath", "Vector Math"),
            ("ShaderNodeMix", "Mix Vector"),
            ("ShaderNodeCombineXYZ", "Combine XYZ"),
            ("ShaderNodeSeparateXYZ", "Separate XYZ"),
            ("ShaderNodeVectorCurve", "Vector Curves"),
            ("ShaderNodeRadialTiling", "Radial Tiling"),
            ("ShaderNodeVectorRotate", "Vector Rotate"),
            ("FunctionNodeCombineCylindrical", "Combine Cylindrical"),
            ("FunctionNodeCombineSpherical", "Combine Spherical"),
            ("FunctionNodeSeparateCylindrical", "Separate Cylindrical"),
            ("FunctionNodeSeparateSpherical", "Separate Spherical"),
        ],
        "Bundle": [
            ("NodeCombineBundle", "Combine Bundle"),
            ("NodeSeparateBundle", "Separate Bundle"),
            ("NodeJoinBundle", "Join Bundle"),
        ],
        "Closure": [
            ("QUICKNODES_OT_add_closure_zone", "Closure"),
            ("NodeEvaluateClosure", "Evaluate Closure"),
        ],
        "Field": [
            ("GeometryNodeAccumulateField", "Accumulate Field"),
            ("GeometryNodeFieldAtIndex", "Evaluate at Index"),
            ("GeometryNodeFieldOnDomain", "Evaluate on Domain"),
            ("GeometryNodeFieldAverage", "Field Average"),
            ("GeometryNodeFieldMinAndMax", "Field Min & Max"),
            ("GeometryNodeFieldVariance", "Field Variance"),
        ],
        "Matrix": [
            ("FunctionNodeCombineMatrix", "Combine Matrix"),
            ("FunctionNodeCombineTransform", "Combine Transform"),
            ("FunctionNodeMatrixDeterminant", "Determinant"),
            ("FunctionNodeInvertMatrix", "Invert Matrix"),
            ("FunctionNodeMatrixMultiply", "Multiply Matrices"),
            ("FunctionNodeProjectPoint", "Project Point"),
            ("FunctionNodeSeparateMatrix", "Separate Matrix"),
            ("FunctionNodeSeparateTransform", "Separate Transform"),
            ("FunctionNodeTransformDirection", "Transform Direction"),
            ("FunctionNodeTransformPoint", "Transform Point"),
            ("FunctionNodeTransposeMatrix", "Transpose Matrix"),
        ],
        "Rotation": [
            ("FunctionNodeAlignRotationToVector", "Align Rotation to Vector"),
            ("FunctionNodeAxesToRotation", "Axes to Rotation"),
            ("FunctionNodeAxisAngleToRotation", "Axis Angle to Rotation"),
            ("FunctionNodeEulerToRotation", "Euler to Rotation"),
            ("FunctionNodeInvertRotation", "Invert Rotation"),
            ("ShaderNodeMix", "Mix Rotation"),
            ("FunctionNodeRotateRotation", "Rotate Rotation"),
            ("FunctionNodeRotateVector", "Rotate Vector"),
            ("FunctionNodeRotationToAxisAngle", "Rotation to Axis Angle"),
            ("FunctionNodeRotationToEuler", "Rotation to Euler"),
            ("FunctionNodeRotationToQuaternion", "Rotation to Quaternion"),
            ("FunctionNodeQuaternionToRotation", "Quaternion to Rotation"),
        ],
        "Deprecated": [
            ("FunctionNodeAlignEulerToVector", "Align Euler to Vector"),
            ("FunctionNodeRotateEuler", "Rotate Euler"),
        ],
    },
    "GROUP": [
        ("NodeGroupInput", "Group Input"),
        ("NodeGroupOutput", "Group Output"),
    ],
    "LAYOUT": [
        ("NodeFrame", "Frame"),
        ("NodeReroute", "Reroute"),
    ],
    "GREASE PENCIL": {
        "Read": [
            ("GeometryNodeInputNamedLayerSelection", "Named Layer Selection"),
        ],
        "Write": [
            ("GeometryNodeSetGreasePencilColor", "Set Grease Pencil Color"),
            ("GeometryNodeSetGreasePencilDepth", "Set Grease Pencil Depth"),
            ("GeometryNodeSetGreasePencilSoftness", "Set Grease Pencil Softness"),
        ],
        "Operations": [
            ("GeometryNodeGreasePencilToCurves", "Grease Pencil to Curves"),
            ("GeometryNodeMergeLayers", "Merge Layers"),
        ],
    },
    "HAIR": {
        "Deformation": [
            ("GeometryNodeBlendHairCurves", "Blend Hair Curves"),
            ("GeometryNodeDisplaceHairCurves", "Displace Hair Curves"),
            ("GeometryNodeFrizzHairCurves", "Frizz Hair Curves"),
            ("GeometryNodeHairCurvesNoise", "Hair Curves Noise"),
            ("GeometryNodeRollHairCurves", "Roll Hair Curves"),
            ("GeometryNodeRotateHairCurves", "Rotate Hair Curves"),
            ("GeometryNodeShrinkwrapHairCurves", "Shrinkwrap Hair Curves"),
            ("GeometryNodeSmoothHairCurves", "Smooth Hair Curves"),
            ("GeometryNodeStraightenHairCurves", "Straighten Hair Curves"),
            ("GeometryNodeTrimHairCurves", "Trim Hair Curves"),
        ],
        "Generation": [
            ("GeometryNodeDuplicateHairCurves", "Duplicate Hair Curves"),
            ("GeometryNodeGenerateHairCurves", "Generate Hair Curves"),
            ("GeometryNodeInterpolateHairCurves", "Interpolate Hair Curves"),
        ],
        "Guides": [
            ("GeometryNodeBraidHairCurves", "Braid Hair Curves"),
            ("GeometryNodeClumpHairCurves", "Clump Hair Curves"),
            ("GeometryNodeCreateGuideIndexMap", "Create Guide Index Map"),
            ("GeometryNodeCurlHairCurves", "Curl Hair Curves"),
        ],
        "Read": [
            ("GeometryNodeInputCurveInfo", "Curve Info"),
            ("GeometryNodeInputCurveRoot", "Curve Root"),
            ("GeometryNodeInputCurveSegment", "Curve Segment"),
            ("GeometryNodeInputCurveTip", "Curve Tip"),
            ("GeometryNodeHairAttachmentInfo", "Hair Attachment Info"),
        ],
        "Utility": [
            ("GeometryNodeAttachHairCurvesToSurface", "Attach Hair Curves to Surface"),
            ("GeometryNodeRedistributeCurvePoints", "Redistribute Curve Points"),
            ("GeometryNodeRestoreCurveSegmentLength", "Restore Curve Segment Length"),
        ],
        "Write": [
            ("GeometryNodeSetHairCurveProfile", "Set Hair Curve Profile"),
        ],
    },
    "NORMALS": [
        ("GeometryNodeSmoothByAngle", "Smooth by Angle"),
    ],
}

# Flatten all nodes for search functionality
ALL_NODES = []
for category, content in NODE_CATEGORIES.items():
    if isinstance(content, dict):
        for subcategory, nodes in content.items():
            for node in nodes:
                ALL_NODES.append(node)
    else:
        for node in content:
            ALL_NODES.append(node)

# Properties for search functionality
class QuickNodesProperties(PropertyGroup):
    search_filter: StringProperty(
        name="Search Filter",
        description="Filter nodes by name",
        default=""
    )

# Function to deselect all nodes
def deselect_all_nodes(context):
    """Deselect all nodes in the current node tree"""
    space = context.space_data
    if space.type == 'NODE_EDITOR' and space.edit_tree:
        for node in space.edit_tree.nodes:
            node.select = False

# Operator to add a node to the active node tree
class QUICKNODES_OT_add_node(Operator):
    bl_idname = "quicknodes.add_node"
    bl_label = "Add Node"
    bl_description = "Add a node to the active node tree"
    
    node_type: StringProperty()
    
    def execute(self, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.edit_tree:
            node_tree = space.edit_tree
            
            # Deselect all existing nodes
            deselect_all_nodes(context)
            
            # Create the node
            node = node_tree.nodes.new(type=self.node_type)
            
            # Place node 800 units to the left of cursor location
            cursor_loc = context.space_data.cursor_location
            node.location = (cursor_loc[0] - 800, cursor_loc[1])
            
            # Select the newly created node
            node.select = True
            node_tree.nodes.active = node
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree found")
            return {'CANCELLED'}

# DEFINE FUNCTIONS FOR NODE PAIRS
# ============================================================================

class QUICKNODES_OT_add_simulation_zone(Operator):
    bl_idname = "quicknodes.add_simulation_zone"
    bl_label = "Simulation Zone"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.edit_tree:
            tree = space.edit_tree
            cursor_loc = space.cursor_location
            
            # Deselect all existing nodes
            deselect_all_nodes(context)
            
            # Create the simulation zone nodes
            node_input = tree.nodes.new("GeometryNodeSimulationInput")
            node_output = tree.nodes.new("GeometryNodeSimulationOutput")
            
            # Position the nodes horizontally (input on left, output on right)
            node_input.location = (cursor_loc[0] - 900, cursor_loc[1])
            node_output.location = (cursor_loc[0] - 700, cursor_loc[1])
            
            # Pair the nodes
            node_input.pair_with_output(node_output)
            
            # Select both nodes in the pair for easy movement
            node_input.select = True
            node_output.select = True
            tree.nodes.active = node_input
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree found")
            return {'CANCELLED'}


class QUICKNODES_OT_add_foreach_element_zone(Operator):
    bl_idname = "quicknodes.add_foreach_element_zone"
    bl_label = "For Each Element"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.edit_tree:
            tree = space.edit_tree
            cursor_loc = space.cursor_location
            
            # Deselect all existing nodes
            deselect_all_nodes(context)
            
            # Create the for each element nodes
            node_input = tree.nodes.new("GeometryNodeForeachGeometryElementInput")
            node_output = tree.nodes.new("GeometryNodeForeachGeometryElementOutput")
            
            # Position the nodes horizontally (input on left, output on right)
            node_input.location = (cursor_loc[0] - 900, cursor_loc[1])
            node_output.location = (cursor_loc[0] - 700, cursor_loc[1])
            
            # Pair the nodes
            node_input.pair_with_output(node_output)
            
            # Select both nodes in the pair for easy movement
            node_input.select = True
            node_output.select = True
            tree.nodes.active = node_input
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree found")
            return {'CANCELLED'}
    
    
class QUICKNODES_OT_add_repeat_zone(Operator):
    bl_idname = "quicknodes.add_repeat_zone"
    bl_label = "Repeat"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.edit_tree:
            tree = space.edit_tree
            cursor_loc = space.cursor_location
            
            # Deselect all existing nodes
            deselect_all_nodes(context)
            
            # Create the repeat zone nodes
            node_input = tree.nodes.new("GeometryNodeRepeatInput")
            node_output = tree.nodes.new("GeometryNodeRepeatOutput")
            
            # Position the nodes horizontally (input on left, output on right)
            node_input.location = (cursor_loc[0] - 900, cursor_loc[1])
            node_output.location = (cursor_loc[0] - 700, cursor_loc[1])
            
            # Pair the nodes
            node_input.pair_with_output(node_output)
            
            # Select both nodes in the pair for easy movement
            node_input.select = True
            node_output.select = True
            tree.nodes.active = node_input
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree found")
            return {'CANCELLED'}
            
class QUICKNODES_OT_add_closure_zone(Operator):
    bl_idname = "quicknodes.add_closure_zone"
    bl_label = "Repeat"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        space = context.space_data
        if space.type == 'NODE_EDITOR' and space.edit_tree:
            tree = space.edit_tree
            cursor_loc = space.cursor_location
            
            # Deselect all existing nodes
            deselect_all_nodes(context)
            
            # Create the closure zone nodes
            node_input = tree.nodes.new("NodeClosureInput")
            node_output = tree.nodes.new("NodeClosureOutput")
            
            # Position the nodes horizontally (input on left, output on right)
            node_input.location = (cursor_loc[0] - 900, cursor_loc[1])
            node_output.location = (cursor_loc[0] - 700, cursor_loc[1])
            
            # Pair the nodes
            node_input.pair_with_output(node_output)
            
            # Select both nodes in the pair for easy movement
            node_input.select = True
            node_output.select = True
            tree.nodes.active = node_input
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree found")
            return {'CANCELLED'}

# Function to draw nodes in a 2-column layout
def draw_nodes_two_column(layout, nodes):
    col = layout.column(align=True)
    row = col.row()
    
    # Create two columns
    col1 = row.column()
    col2 = row.column()
    
    # Distribute nodes between the two columns
    for i, node in enumerate(nodes):
        node_type, node_name = node
        col = col1 if i % 2 == 0 else col2
        
        # Check if this is a custom operator or a regular node
        if node_type.startswith("QUICKNODES_OT_"):
            # Create operator button for custom operators
            op = col.operator(node_type, text=node_name)
        else:
            # Create operator button for regular nodes
            op = col.operator("quicknodes.add_node", text=node_name)
            op.node_type = node_type

# Base panel class for all Quick Nodes panels
class QuickNodesPanel:
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Quick Nodes"

# Main panel
class NODE_PT_quick_nodes_main(QuickNodesPanel, Panel):
    bl_label = "Quick Nodes"
    bl_idname = "NODE_PT_quick_nodes_main"
    
    def draw(self, context):
        layout = self.layout
        
        # Check if there's an active node tree
        space = context.space_data
        if space.type != 'NODE_EDITOR' or not space.edit_tree:
            # Display message when no active node tree
            col = layout.column(align=True)
            col.label(text="No active node tree", icon='ERROR')
            col.separator()
            col.label(text="To use Quick Nodes:")
            col.label(text="Create or open a Geometry Nodes setup")
            return

# Search panel
class NODE_PT_quick_nodes_search(QuickNodesPanel, Panel):
    bl_label = "SEARCH"
    bl_idname = "NODE_PT_quick_nodes_search"
    bl_parent_id = "NODE_PT_quick_nodes_main"
        
    def draw(self, context):
        layout = self.layout
        
        # Check if there's an active node tree
        space = context.space_data
        if space.type != 'NODE_EDITOR' or not space.edit_tree:
            # Don't show search if no active node tree
            return
            
        # Check if the property exists, if not create it
        if not hasattr(context.scene, 'quick_nodes_props'):
            return
            
        props = context.scene.quick_nodes_props
        
        # Search box
        layout.prop(props, "search_filter", text="", icon='VIEWZOOM')
        
        # Show search results if there's a search term
        if props.search_filter:
            layout.separator()
            search_term = props.search_filter.lower()
            
            # Filter nodes based on search term
            results = [node for node in ALL_NODES if search_term in node[1].lower()]
            
            if results:
                box = layout.box()
                box.label(text=f"Results ({len(results)}):", icon='ZOOM_IN')
                draw_nodes_two_column(box, results[:30])  # Limit to 30 results
                if len(results) > 30:
                    box.label(text=f"...and {len(results) - 30} more")
            else:
                layout.label(text="No results found", icon='INFO')

# Quick Favorites panel
class NODE_PT_quick_nodes_favorites(QuickNodesPanel, Panel):
    bl_label = "FAVORITES"
    bl_idname = "NODE_PT_quick_nodes_favorites"
    bl_parent_id = "NODE_PT_quick_nodes_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Check if there's an active node tree
        space = context.space_data
        if space.type != 'NODE_EDITOR' or not space.edit_tree:
            # Don't show favorites if no active node tree
            return
        
        # Get favorites from Blender's workspace tools
        favorites = []
        
        try:
            # Access the node editor's favorites
            wm = context.window_manager
            if hasattr(wm, 'operators'):
                # Check for node add search favorites
                for item in wm.operators:
                    if hasattr(item, 'name'):
                        pass
            
            # Try to get from workspace tool settings
            workspace = context.workspace
            if workspace:
                # Blender stores favorites in the workspace
                pass
                
        except Exception as e:
            pass
        
        # If we can't find favorites, show a helpful message
        if not favorites:
            col = layout.column(align=True)
            col.label(text="No favorites set", icon='SOLO_OFF')
            col.separator()
            col.label(text="To add favorites:", icon='INFO')
            col.label(text="1. Press Shift+A in node editor")
            col.label(text="2. Right-click on any node")
            col.label(text="3. Select 'Add to Quick Favorites'")
        else:
            draw_nodes_two_column(layout, favorites)

# Function to create category panels dynamically
def create_category_panels():
    panels = []
    
    for category_name, category_content in NODE_CATEGORIES.items():
        # Create main category panel
        class_name = f"NODE_PT_quick_nodes_{category_name.lower().replace(' ', '_')}"
        
        # Create a closure to capture the category content
        def make_draw_method(content):
            def draw(self, context):
                # Check if there's an active node tree
                space = context.space_data
                if space.type != 'NODE_EDITOR' or not space.edit_tree:
                    # Don't show nodes if no active node tree
                    return
                    
                if isinstance(content, dict):
                    # Draw main nodes first if they exist
                    if "Main Nodes" in content:
                        main_nodes = content["Main Nodes"]
                        if main_nodes:
                            draw_nodes_two_column(self.layout, main_nodes)
                            self.layout.separator()
                else:
                    # This is a simple list of nodes
                    draw_nodes_two_column(self.layout, content)
            return draw
        
        panel_class = type(
            class_name,
            (QuickNodesPanel, Panel),
            {
                "bl_label": category_name,
                "bl_idname": class_name,
                "bl_parent_id": "NODE_PT_quick_nodes_main",
                "bl_options": {'DEFAULT_CLOSED'},
                "draw": make_draw_method(category_content)
            }
        )
        panels.append(panel_class)
        
        # If category has subcategories, create subcategory panels
        if isinstance(category_content, dict):
            for subcategory_name, nodes in category_content.items():
                # Skip "Main Nodes" as they're already displayed in the main panel
                if subcategory_name == "Main Nodes":
                    continue
                    
                sub_class_name = f"NODE_PT_quick_nodes_{category_name.lower().replace(' ', '_')}_{subcategory_name.lower().replace(' ', '_')}"
                
                # Create a closure to capture the nodes
                def make_sub_draw_method(node_list):
                    def draw(self, context):
                        # Check if there's an active node tree
                        space = context.space_data
                        if space.type != 'NODE_EDITOR' or not space.edit_tree:
                            # Don't show nodes if no active node tree
                            return
                            
                        draw_nodes_two_column(self.layout, node_list)
                    return draw
                
                sub_panel_class = type(
                    sub_class_name,
                    (QuickNodesPanel, Panel),
                    {
                        "bl_label": subcategory_name,
                        "bl_idname": sub_class_name,
                        "bl_parent_id": class_name,
                        "bl_options": {'DEFAULT_CLOSED'},
                        "draw": make_sub_draw_method(nodes)
                    }
                )
                panels.append(sub_panel_class)
    
    return panels

# Create all category panels
category_panels = create_category_panels()

# Register all classes
classes = (
    QuickNodesProperties,
    QUICKNODES_OT_add_node,
    QUICKNODES_OT_add_simulation_zone,
    QUICKNODES_OT_add_foreach_element_zone,
    QUICKNODES_OT_add_repeat_zone,
    QUICKNODES_OT_add_closure_zone,
    NODE_PT_quick_nodes_main,
    NODE_PT_quick_nodes_search,
    NODE_PT_quick_nodes_favorites,
) + tuple(category_panels)

def register():
    # Register the property first
    bpy.utils.register_class(QuickNodesProperties)
    bpy.types.Scene.quick_nodes_props = bpy.props.PointerProperty(type=QuickNodesProperties)
    
    # Then register the other classes
    for cls in classes[1:]:  # Skip QuickNodesProperties as it's already registered
        bpy.utils.register_class(cls)

def unregister():
    # Unregister in reverse order
    for cls in reversed(classes[1:]):  # Skip QuickNodesProperties for now
        bpy.utils.unregister_class(cls)
    
    # Remove the property
    if hasattr(bpy.types.Scene, 'quick_nodes_props'):
        del bpy.types.Scene.quick_nodes_props
    
    # Finally unregister the property class
    bpy.utils.unregister_class(QuickNodesProperties)

if __name__ == "__main__":
    register()
