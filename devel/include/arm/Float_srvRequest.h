// Generated by gencpp from file arm/Float_srvRequest.msg
// DO NOT EDIT!


#ifndef ARM_MESSAGE_FLOAT_SRVREQUEST_H
#define ARM_MESSAGE_FLOAT_SRVREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace arm
{
template <class ContainerAllocator>
struct Float_srvRequest_
{
  typedef Float_srvRequest_<ContainerAllocator> Type;

  Float_srvRequest_()
    : data(0.0)  {
    }
  Float_srvRequest_(const ContainerAllocator& _alloc)
    : data(0.0)  {
  (void)_alloc;
    }



   typedef double _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::arm::Float_srvRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::arm::Float_srvRequest_<ContainerAllocator> const> ConstPtr;

}; // struct Float_srvRequest_

typedef ::arm::Float_srvRequest_<std::allocator<void> > Float_srvRequest;

typedef boost::shared_ptr< ::arm::Float_srvRequest > Float_srvRequestPtr;
typedef boost::shared_ptr< ::arm::Float_srvRequest const> Float_srvRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::arm::Float_srvRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::arm::Float_srvRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::arm::Float_srvRequest_<ContainerAllocator1> & lhs, const ::arm::Float_srvRequest_<ContainerAllocator2> & rhs)
{
  return lhs.data == rhs.data;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::arm::Float_srvRequest_<ContainerAllocator1> & lhs, const ::arm::Float_srvRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace arm

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::arm::Float_srvRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::arm::Float_srvRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::arm::Float_srvRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::arm::Float_srvRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::arm::Float_srvRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::arm::Float_srvRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::arm::Float_srvRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fdb28210bfa9d7c91146260178d9a584";
  }

  static const char* value(const ::arm::Float_srvRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xfdb28210bfa9d7c9ULL;
  static const uint64_t static_value2 = 0x1146260178d9a584ULL;
};

template<class ContainerAllocator>
struct DataType< ::arm::Float_srvRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "arm/Float_srvRequest";
  }

  static const char* value(const ::arm::Float_srvRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::arm::Float_srvRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 data\n"
;
  }

  static const char* value(const ::arm::Float_srvRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::arm::Float_srvRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Float_srvRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::arm::Float_srvRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::arm::Float_srvRequest_<ContainerAllocator>& v)
  {
    s << indent << "data: ";
    Printer<double>::stream(s, indent + "  ", v.data);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ARM_MESSAGE_FLOAT_SRVREQUEST_H
